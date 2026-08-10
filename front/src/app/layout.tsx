import type { Metadata } from "next";
import ReduxProvider from "@/components/ReduxProvider/ReduxProvider";

export const metadata: Metadata = {
  title: "Stripe Sandbox Example",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <ReduxProvider>
          {children}
        </ReduxProvider>
      </body>
    </html>
  );
}
