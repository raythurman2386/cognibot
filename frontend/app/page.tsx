import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <header className="text-center py-16">
        <h1 className="text-4xl font-bold">Welcome to CogniBot</h1>
        <p className="mt-4 text-lg">
          Your friendly Discord bot powered by OpenAI's API for text and image
          generation.
        </p>
        <a
          href="#subscription"
          className="mt-8 inline-block bg-blue-500 text-white px-6 py-3 rounded-full text-lg font-semibold hover:bg-blue-600"
        >
          Subscribe to Updates
        </a>
      </header>

      <section id="subscription" className="bg-gray-900 text-white py-16">
        <div className="container mx-auto text-center">
          <h2 className="text-2xl font-bold mb-4">
            Subscribe to CogniBot Updates
          </h2>
          <p className="text-lg mb-8">
            Stay informed about the latest features and improvements.
          </p>
        </div>
      </section>
    </main>
  );
}
