import React from 'react'
import { Link } from 'react-router-dom'

export default function PostCard({ post }) {
  return (
    <article className="card post-preview">
      <h2>
        <Link to={`/posts/${post.slug}`}>{post.title}</Link>
      </h2>
      <div className="post-meta">
        by {post.author?.username} &middot;{' '}
        {new Date(post.created_at).toLocaleDateString()}
        {!post.published && <span className="status-badge" style={{ marginLeft: 8 }}>Draft</span>}
      </div>
      {post.categories?.map((c) => (
        <span key={c.id} className="tag">{c.name}</span>
      ))}
      {post.summary && <p>{post.summary}</p>}
      <Link to={`/posts/${post.slug}`}>Read more &rarr;</Link>
    </article>
  )
}
