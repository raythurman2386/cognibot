import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
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
