import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import client from '../api/client'

export default function PostEditor() {
  const { postId } = useParams() // present only in edit mode
  const isEdit = Boolean(postId)
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [summary, setSummary] = useState('')
  const [content, setContent] = useState('')
  const [published, setPublished] = useState(true)
  const [categories, setCategories] = useState([])
  const [selectedCategoryIds, setSelectedCategoryIds] = useState([])
  const [newCategory, setNewCategory] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    client.get('/api/categories').then((res) => setCategories(res.data))
  }, [])

  useEffect(() => {
    if (!isEdit) return
    client.get(`/api/posts/by-id/${postId}`).catch(() => {}) // no-op fallback
  }, [isEdit, postId])

  // Fetch existing post for editing (by id, via slug lookup workaround not needed:
  // we search the full list since /api/posts/{slug} expects a slug, not id)
  useEffect(() => {
    if (!isEdit) return
    client.get('/api/posts', { params: { published_only: false, limit: 100 } }).then((res) => {
      const existing = res.data.find((p) => String(p.id) === String(postId))
      if (existing) {
        client.get(`/api/posts/${existing.slug}`).then((r) => {
          const p = r.data
          setTitle(p.title)
          setSummary(p.summary || '')
          setContent(p.content)
          setPublished(p.published)
          setSelectedCategoryIds(p.categories.map((c) => c.id))
        })
      }
    })
  }, [isEdit, postId])

  function toggleCategory(id) {
    setSelectedCategoryIds((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    )
  }

  async function handleAddCategory() {
    if (!newCategory.trim()) return
    try {
      const res = await client.post('/api/categories', { name: newCategory.trim() })
      setCategories([...categories, res.data])
      setSelectedCategoryIds([...selectedCategoryIds, res.data.id])
      setNewCategory('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not add category')
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    const payload = {
      title,
      summary,
      content,
      published,
      category_ids: selectedCategoryIds,
    }
    try {
      if (isEdit) {
        const res = await client.put(`/api/posts/${postId}`, payload)
        navigate(`/posts/${res.data.slug}`)
      } else {
        const res = await client.post('/api/posts', payload)
        navigate(`/posts/${res.data.slug}`)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not save post')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: 700, margin: '0 auto' }}>
        <h1>{isEdit ? 'Edit Post' : 'New Post'}</h1>
        {error && <div className="error-box" style={{ marginBottom: 14 }}>{error}</div>}
        <form className="stack" style={{ maxWidth: '100%' }} onSubmit={handleSubmit}>
          <div>
            <label>Title</label>
            <input value={title} onChange={(e) => setTitle(e.target.value)} required minLength={3} />
          </div>
          <div>
            <label>Summary (optional)</label>
            <input value={summary} onChange={(e) => setSummary(e.target.value)} maxLength={500} />
          </div>
          <div>
            <label>Content</label>
            <textarea value={content} onChange={(e) => setContent(e.target.value)} required style={{ minHeight: 220 }} />
          </div>
          <div>
            <label>Categories</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 8 }}>
              {categories.map((c) => (
                <label key={c.id} style={{ display: 'flex', alignItems: 'center', gap: 4, fontWeight: 400 }}>
                  <input
                    type="checkbox"
                    style={{ width: 'auto' }}
                    checked={selectedCategoryIds.includes(c.id)}
                    onChange={() => toggleCategory(c.id)}
                  />
                  {c.name}
                </label>
              ))}
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                placeholder="New category name"
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
              />
              <button type="button" className="btn secondary" onClick={handleAddCategory}>Add</button>
            </div>
          </div>
          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <input
                type="checkbox"
                style={{ width: 'auto' }}
                checked={published}
                onChange={(e) => setPublished(e.target.checked)}
              />
              Publish immediately (uncheck to save as draft)
            </label>
          </div>
          <button className="btn" type="submit" disabled={submitting}>
            {submitting ? 'Saving...' : isEdit ? 'Save Changes' : 'Publish Post'}
          </button>
        </form>
      </div>
    </div>
  )
}
