'use client'

import { useState } from 'react'
import Image from 'next/image'
import { createClient } from '@/lib/supabase/client'

type UploadState = 'idle' | 'uploading' | 'done' | 'error'

export default function ReceiptUpload() {
  const [progress, setProgress] = useState(0)
  const [state, setState] = useState<UploadState>('idle')
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setPreviewUrl(URL.createObjectURL(file))
    setState('uploading')
    setProgress(0)
    setError(null)

    const filename = `${Date.now()}-${Math.random().toString(36).slice(2)}.${file.name.split('.').pop()}`
    const supabase = createClient()

    // סימולציה של progress (Supabase JS אינו חושף progress events)
    const interval = setInterval(() => {
      setProgress((p) => Math.min(p + 15, 90))
    }, 150)

    const { error: uploadError } = await supabase.storage
      .from('receipts')
      .upload(filename, file, { contentType: file.type })

    clearInterval(interval)

    if (uploadError) {
      setState('error')
      setError(uploadError.message)
      setProgress(0)
    } else {
      setProgress(100)
      setState('done')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-2xl shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-center">העלאת קבלה</h2>

      <label className="flex flex-col items-center justify-center w-full h-36 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-blue-400 hover:bg-blue-50 transition-colors">
        <span className="text-4xl mb-2">📷</span>
        <span className="text-sm text-gray-500">בחרו תמונה מהמכשיר</span>
        <input
          type="file"
          accept="image/*"
          className="hidden"
          onChange={handleFileChange}
        />
      </label>

      {state === 'uploading' && (
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-500 mb-1">
            <span>מעלה...</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all duration-200"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {state === 'error' && (
        <p className="mt-4 text-red-500 text-sm text-center">{error}</p>
      )}

      {state === 'done' && previewUrl && (
        <div className="mt-4">
          <p className="text-green-600 text-sm text-center mb-3">הקבלה הועלתה בהצלחה</p>
          <div className="relative w-full h-64 rounded-xl overflow-hidden border">
            <Image
              src={previewUrl}
              alt="תצוגה מקדימה"
              fill
              className="object-contain"
            />
          </div>
        </div>
      )}
    </div>
  )
}
