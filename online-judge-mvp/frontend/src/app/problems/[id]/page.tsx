'use client'

import { useEffect, useState } from 'react'
import Editor from '@monaco-editor/react'

interface Problem {
  id: number
  title: string
  description: string
  sample_input?: string
  sample_output?: string
}

interface Submission {
  id: number
  stdout?: string
  stderr?: string
  status: string
  time?: number
}

export default function ProblemPage({ params }: { params: { id: string } }) {
  const [problem, setProblem] = useState<Problem | null>(null)
  const [code, setCode] = useState('')
  const [stdin, setStdin] = useState('')
  const [sub, setSub] = useState<Submission | null>(null)
  const API = process.env.NEXT_PUBLIC_API_URL

  useEffect(() => {
    fetch(`${API}/problems/${params.id}`)
      .then(res => res.json())
      .then(setProblem)
  }, [params.id, API])

  const submit = async () => {
    const res = await fetch(`${API}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem_id: Number(params.id), code, stdin })
    })
    const data: Submission = await res.json()
    setSub(data)
    if (res.ok) poll(data.id)
  }

  const poll = async (id: number) => {
    let result: Submission
    do {
      await new Promise(r => setTimeout(r, 1000))
      const res = await fetch(`${API}/submissions/${id}`)
      result = await res.json()
      setSub(result)
    } while (result.status === 'Queued' || result.status === 'Processing')
  }

  return (
    <div className='p-4'>
      <h1 className='text-2xl font-bold'>{problem?.title}</h1>
      <p className='whitespace-pre-wrap'>{problem?.description}</p>
      <div className='my-4'>
        <Editor height='40vh' defaultLanguage='python' value={code} onChange={(v) => setCode(v || '')} />
      </div>
      <textarea className='w-full border p-2' rows={5} placeholder='stdin' value={stdin} onChange={e => setStdin(e.target.value)} />
      <button className='mt-2 px-4 py-2 bg-blue-500 text-white' onClick={submit}>Run</button>
      {sub && (
        <table className='mt-4 table-auto border'>
          <tbody>
            <tr><th className='px-2 text-left'>Status</th><td>{sub.status}</td></tr>
            <tr><th className='px-2 text-left'>Time</th><td>{sub.time}</td></tr>
            <tr><th className='px-2 text-left'>stdout</th><td><pre>{sub.stdout}</pre></td></tr>
            <tr><th className='px-2 text-left'>stderr</th><td><pre>{sub.stderr}</pre></td></tr>
          </tbody>
        </table>
      )}
    </div>
  )
}
