import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem',
    backgroundColor: 'var(--neutral-white)',
    color: 'var(--neutral-black)',
    borderBottom: '2px solid var(--primary-skyblue)',
    position: 'sticky',
    top: 0,
    zIndex: 1000,
    boxShadow: '0 2px 10px rgba(0,0,0,0.05)'
  };

  const linksStyle = {
    display: 'flex',
    gap: '12px',
    alignItems: 'center'
  };

  const linkStyle = {
    color: 'var(--neutral-black)',
    textDecoration: 'none',
    fontWeight: '600',
    fontSize: '0.9rem'
  };

  return (
    <nav style={navStyle}>
      <Link to="/" style={{ ...linkStyle, fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-maroon)' }}>
        Declutter254
      </Link>

      <div style={linksStyle}>
        {user ? (
          <>
            <button
              onClick={handleLogout}
              className="btn-accent"
              style={{
                padding: '6px 12px',
                fontSize: '0.8rem'
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link style={linkStyle} to="/login">Login</Link>
            <Link style={{ ...linkStyle, color: 'var(--primary-skyblue)' }} to="/signup">Join</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;