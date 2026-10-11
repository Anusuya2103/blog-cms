import React, { useEffect, useState } from 'react'
import client from '../api/client'
import PostCard from '../components/PostCard.jsx'

export default function Home() {
  const [posts, setPosts] = useState([])
  const [categories, setCategories] = useState([])
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    client.get('/api/categories').then((res) => setCategories(res.data)).catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    const params = {}
    if (search) params.search = search
    if (category) params.category = category
    client
      .get('/api/posts', { params })
      .then((res) => setPosts(res.data))
      .catch(() => setError('Could not load posts. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [search, category])

  return (
    <div className="container">
      <div style={{ display: 'flex', gap: 12, marginBottom: 24, flexWrap: 'wrap' }}>
        <input
          placeholder="Search posts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ maxWidth: 280 }}
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ maxWidth: 200 }}>
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.slug}>{c.name}</option>
          ))}
        </select>
      </div>

      {error && <div className="error-box">{error}</div>}
      {loading && <p>Loading posts...</p>}
      {!loading && posts.length === 0 && !error && (
        <div className="empty-state">No posts yet. Be the first to publish one!</div>
      )}
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  )
}
