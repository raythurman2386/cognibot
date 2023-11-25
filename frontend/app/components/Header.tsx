import Link from "next/link";

export default function Header() {
    return (
                <header className="text-center py-16">
          <h1 className="text-4xl font-bold">Welcome to CogniBot</h1>
          <p className="mt-4 text-lg">
            Your friendly Discord bot powered by OpenAI&apos;s API for text and image
            generation.
          </p>
          <Link
            href="/#subscription"
            className="mt-8 inline-block bg-blue-500 text-white px-6 py-3 rounded-full text-lg font-semibold hover:bg-blue-600"
          >
            Subscribe to Updates
          </Link>
        </header>
    )
}