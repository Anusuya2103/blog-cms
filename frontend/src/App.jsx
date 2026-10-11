import React, { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Header from './components/Header.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import PostDetail from './pages/PostDetail.jsx'
import PostEditor from './pages/PostEditor.jsx'
import client from './api/client'

export default function App() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    client
      .get('/api/health')
      .then((res) => setHealth(res.data))
      .catch(() => setHealth({ status: 'down', database: 'unreachable' }))
  }, [])

  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/posts/:slug" element={<PostDetail />} />
          <Route
            path="/new-post"
            element={
              <ProtectedRoute roles={['admin', 'author']}>
                <PostEditor />
              </ProtectedRoute>
            }
          />
          <Route
            path="/edit-post/:postId"
            element={
              <ProtectedRoute roles={['admin', 'author']}>
                <PostEditor />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
      {health && (
        <div className="health-strip">
          API: {health.status} &middot; DB: {health.database}
        </div>
      )}
    </>
  )
}
