import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Header() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/')
  }

  return (
    <header className="site-header">
      <div className="header-inner">
        <Link to="/" className="brand">📝 BlogCMS</Link>
        <nav className="main-nav">
          <Link to="/">Home</Link>
          {user && (user.role === 'admin' || user.role === 'author') && (
            <Link to="/new-post">New Post</Link>
          )}
          {user ? (
            <>
              <span style={{ fontSize: '0.85rem', color: '#5b6470' }}>
                {user.username} <span className="tag">{user.role}</span>
              </span>
              <button className="btn secondary" onClick={handleLogout}>Log out</button>
            </>
          ) : (
            <>
              <Link to="/login">Log in</Link>
              <Link to="/register" className="btn">Sign up</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
