import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { PlusCircle, LayoutDashboard, LogOut } from 'lucide-react';

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
    padding: '1rem 2rem',
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
    gap: '24px',
    alignItems: 'center'
  };

  const linkStyle = {
    color: 'var(--neutral-black)',
    textDecoration: 'none',
    fontWeight: '600',
    fontSize: '0.9rem',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    transition: 'color 0.2s ease'
  };

  return (
    <nav style={navStyle}>
      <Link to="/" style={{ ...linkStyle, fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-maroon)' }}>
        Declutter254
      </Link>

      <div style={linksStyle}>
        {user ? (
          <>
            <Link style={linkStyle} to="/post-item">
              <PlusCircle size={20} color="var(--primary-skyblue)" />
              <span>Give Item</span>
            </Link>
            <Link style={linkStyle} to="/dashboard">
              <LayoutDashboard size={20} />
              <span>Dashboard</span>
            </Link>
            <button
              onClick={handleLogout}
              className="btn-accent"
              style={{
                padding: '8px 16px',
                fontSize: '0.85rem',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                borderRadius: '8px'
              }}
            >
              <LogOut size={18} />
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