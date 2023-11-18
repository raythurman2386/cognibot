import Image from "next/image";

export default function Terms() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <section id="terms" className="container mx-auto my-8">
        <h1 className="text-3xl font-bold mb-4">CogniBot - Terms of Service</h1>

        <p className="mb-4">
          By using CogniBot, you agree to comply with and be bound by the
          following terms and conditions:
        </p>

        <h2 className="text-xl font-semibold mb-2">1. Use of the Service</h2>
        <p className="mb-4">
          You must use CogniBot in compliance with all applicable laws and
          regulations.
        </p>

        <h2 className="text-xl font-semibold mb-2">2. Data Privacy</h2>
        <p className="mb-4">
          We respect your privacy. Our Privacy Policy outlines how we collect,
          use, and protect your data.
        </p>

        <h2 className="text-xl font-semibold mb-2">3. Prohibited Activities</h2>
        <p className="mb-4">
          You are prohibited from engaging in any activities that may harm the
          service or other users.
        </p>

        <h2 className="text-xl font-semibold mb-2">4. Changes to Terms</h2>
        <p className="mb-4">
          We reserve the right to modify these terms at any time. You are
          responsible for reviewing updates.
        </p>

        <p className="mt-8">Last updated: [Date]</p>
      </section>
    </main>
  );
}
