import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth()

  if (loading) return <div className="container"><p>Loading...</p></div>
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) {
    return (
      <div className="container">
        <div className="error-box">You do not have permission to view this page.</div>
      </div>
    )
  }
  return children
}
