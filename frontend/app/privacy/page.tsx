import Image from "next/image";

export default function Privacy() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <section id="privacy" className="container mx-auto my-8">
        <h1 className="text-3xl font-bold mb-4">CogniBot - Privacy Policy</h1>

        <p className="mb-4">
          This Privacy Policy explains how CogniBot handles your data:
        </p>

        <h2 className="text-xl font-semibold mb-2">1. Data Collection</h2>
        <p className="mb-4">
          CogniBot does not collect or store any user data, including personal
          information.
        </p>

        <h2 className="text-xl font-semibold mb-2">2. Information Usage</h2>
        <p className="mb-4">
          As no user data is collected, there is no information to use for any
          purpose.
        </p>

        <h2 className="text-xl font-semibold mb-2">3. Data Security</h2>
        <p className="mb-4">
          While no user data is collected, we are committed to ensuring the
          security of any potential future data collected.
        </p>

        <h2 className="text-xl font-semibold mb-2">4. Changes to Policy</h2>
        <p className="mb-4">
          We reserve the right to modify this policy. Any changes will be
          reflected on this page.
        </p>

        <p className="mt-8">Last updated: [Date]</p>
      </section>
    </main>
  );
}
