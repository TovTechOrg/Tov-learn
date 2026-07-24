import ReceiptUpload from '@/components/ReceiptUpload'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-black text-center mb-6">חשבונית-בקליק</h1>
        <ReceiptUpload />
      </div>
    </main>
  )
}
