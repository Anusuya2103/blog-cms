import React, { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import client from '../api/client'
import { useAuth } from '../context/AuthContext.jsx'

export default function PostDetail() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [post, setPost] = useState(null)
  const [comments, setComments] = useState([])
  const [newComment, setNewComment] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    client.get(`/api/posts/${slug}`).then((res) => {
      setPost(res.data)
      client.get(`/api/posts/${res.data.id}/comments`).then((r) => setComments(r.data))
    }).catch(() => setError('Post not found'))
  }, [slug])

  async function handleAddComment(e) {
    e.preventDefault()
    if (!newComment.trim()) return
    try {
      const res = await client.post(`/api/posts/${post.id}/comments`, { content: newComment })
      setComments([...comments, res.data])
      setNewComment('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not post comment')
    }
  }

  async function handleDeletePost() {
    if (!window.confirm('Delete this post permanently?')) return
    await client.delete(`/api/posts/${post.id}`)
    navigate('/')
  }

  if (error && !post) return <div className="container"><div className="error-box">{error}</div></div>
  if (!post) return <div className="container"><p>Loading...</p></div>

  const canManage = user && (user.id === post.author.id || user.role === 'admin')

  return (
    <div className="container">
      <article className="card">
        <h1>{post.title}</h1>
        <div className="post-meta">
          by {post.author.username} &middot; {new Date(post.created_at).toLocaleString()}
          {!post.published && <span className="status-badge" style={{ marginLeft: 8 }}>Draft</span>}
        </div>
        {post.categories.map((c) => <span key={c.id} className="tag">{c.name}</span>)}
        <div style={{ marginTop: 18, whiteSpace: 'pre-wrap' }}>{post.content}</div>

        {canManage && (
          <div style={{ marginTop: 24, display: 'flex', gap: 10 }}>
            <Link to={`/edit-post/${post.id}`} className="btn secondary">Edit</Link>
            <button className="btn danger" onClick={handleDeletePost}>Delete</button>
          </div>
        )}
      </article>

      <div className="card">
        <h3>Comments ({comments.length})</h3>
        {comments.map((c) => (
          <div key={c.id} className="comment">
            <strong>{c.author.username}</strong>{' '}
            <span style={{ color: '#5b6470', fontSize: '0.8rem' }}>
              {new Date(c.created_at).toLocaleString()}
            </span>
            <p style={{ margin: '4px 0 0' }}>{c.content}</p>
          </div>
        ))}

        {user ? (
          <form onSubmit={handleAddComment} style={{ marginTop: 16 }}>
            <textarea
              placeholder="Add a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              style={{ minHeight: 80 }}
            />
            <button className="btn" type="submit" style={{ marginTop: 8 }}>Post comment</button>
          </form>
        ) : (
          <p style={{ marginTop: 16 }}>
            <Link to="/login">Log in</Link> to leave a comment.
          </p>
        )}
      </div>
    </div>
  )
}
