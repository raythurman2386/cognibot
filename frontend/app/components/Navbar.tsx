import Link from "next/link";

export default function Navbar() {
    return (
                <nav className="bg-gray-800 p-4">
          <div className="container mx-auto flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold">
              CogniBot
            </Link>
            <div className="space-x-4">
              <Link href="/terms" className="hover:text-gray-300">
                Terms of Service
              </Link>
              <Link href="/privacy" className="hover:text-gray-300">
                Privacy Policy
              </Link>
            </div>
          </div>
        </nav>
    )
}