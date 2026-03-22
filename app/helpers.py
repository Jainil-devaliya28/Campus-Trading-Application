from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from .models import db, Log


# ──────────────────────────────────────────────
# Logging helper
# ──────────────────────────────────────────────
def log_action(action_type: str, description: str, member_id: int = None):
    """Insert a record into the Logs table."""
    try:
        if member_id is None:
            member_id = session.get('member_id')
        entry = Log(member_id=member_id, action_type=action_type, description=description)
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        # If logging fails, don't crash the app
        print(f"Failed to log action: {e}")


def log_security_event(action_type: str, description: str, ip_address: str = None, user_agent: str = None):
    """Log security-related events like unauthorized access attempts."""
    try:
        full_description = f"{description} | IP: {ip_address or 'unknown'} | UA: {user_agent or 'unknown'}"
        entry = Log(member_id=None, action_type=action_type, description=full_description)
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        print(f"Failed to log security event: {e}")


# ──────────────────────────────────────────────
# Auth decorators
# ──────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'member_id' not in session:
            # Log unauthorized access attempt
            ip = request.remote_addr
            ua = request.headers.get('User-Agent', 'unknown')
            log_security_event(
                'UNAUTHORIZED_ACCESS',
                f"Attempted access to {request.path} without authentication",
                ip,
                ua
            )
            # Return JSON for API/poll endpoints
            if request.path.endswith('/poll'):
                return jsonify(error='login required'), 401
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'member_id' not in session:
            ip = request.remote_addr
            ua = request.headers.get('User-Agent', 'unknown')
            log_security_event(
                'UNAUTHORIZED_ADMIN_ACCESS',
                f"Attempted admin access to {request.path} without authentication",
                ip,
                ua
            )
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            name = session.get('name', 'unknown')
            log_security_event(
                'INSUFFICIENT_PRIVILEGES',
                f"{name} (User with ID {session.get('member_id')}) attempted admin access to {request.path}",
                request.remote_addr,
                request.headers.get('User-Agent', 'unknown')
            )
            flash('Admin access required. You do not have permission to view this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


def owner_or_admin_required(get_owner_id_fn):
    """
    Decorator factory. Pass a callable that takes (kwargs) and returns the owner's member_id.
    Usage:
        @owner_or_admin_required(lambda kw: Product.query.get(kw['product_id']).seller_id)
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'member_id' not in session:
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login'))
            owner_id = get_owner_id_fn(kwargs)
            if session['member_id'] != owner_id and session.get('role') != 'admin':
                flash('You do not have permission to perform this action.', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator


# ──────────────────────────────────────────────
# Notification helper
# ──────────────────────────────────────────────
def notify(member_id: int, title: str, message: str, link: str = None):
    """Create an in-app notification for a user."""
    from .models import Notification
    notif = Notification(
        member_id = member_id,
        title     = title,
        message   = message,
        link      = link
    )
    db.session.add(notif)
    db.session.commit()
