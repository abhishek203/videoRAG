'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Button } from './button'
import { Input } from './input'

interface SearchResult {
  timestamp: number
  videoUrl: string
}

export default function VideoSearch() {
  const [query, setQuery] = useState('')
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      // Replace this URL with your actual backend endpoint
      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
      if (!response.ok) {
        throw new Error('Search failed')
      }
      const data: SearchResult = await response.json()
      setSearchResult(data)
    } catch (error) {
      console.error('Error searching:')
      // Handle error (e.g., show error message to user)
    }
  }

  useEffect(() => {
    if (searchResult && videoRef.current) {
      videoRef.current.currentTime = searchResult.timestamp
    }
  }, [searchResult])

  return (
    <div className="max-w-2xl mx-auto p-4">
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <Input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your search query"
          className="flex-grow"
        />
        <Button type="submit">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 mr-2 inline-block"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          Search
        </Button>
      </form>

      {searchResult && (
        <div className="mt-4">
          <video
            ref={videoRef}
            src={searchResult.videoUrl}
            controls
            className="w-full rounded-lg shadow-lg"
          >
            Your browser does not support the video tag.
          </video>
          <p className="mt-2 text-sm text-gray-600">
            Video starts at {searchResult.timestamp} seconds
          </p>
        </div>
      )}
    </div>
  )
}