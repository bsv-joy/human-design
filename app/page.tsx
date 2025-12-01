import Link from "next/link";
import { Mascot } from "./components/Mascot"; // Assuming Mascot is copied or will be created
import { ArrowRight, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative flex flex-col items-center justify-center min-h-[80vh] px-6 text-center overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(212,175,55,0.15)_0%,transparent_70%)] pointer-events-none" />

        <div className="relative z-10 animate-in fade-in zoom-in duration-1000">
          {/* Placeholder for Mascot, assuming it will be created */}
          <div className="w-32 h-32 md:w-48 md:h-48 mb-8 text-gold-400 mx-auto drop-shadow-[0_0_15px_rgba(212,175,55,0.5)] flex items-center justify-center">
            <Sparkles className="w-24 h-24" /> {/* Temporary icon */}
          </div>

          <h1 className="text-5xl md:text-7xl font-bold font-serif mb-6 tracking-tight">
            <span className="text-gradient-gold">Human Designs</span>
          </h1>

          <p className="text-xl md:text-2xl text-zinc-400 max-w-2xl mx-auto mb-10 font-light leading-relaxed">
            Free yourself from the Republic of the Illiterates. <br />
            Forge your own sovereign statements.
          </p>

          <div className="flex flex-col md:flex-row items-center justify-center gap-4">
            <Link
              href="/manifesto"
              className="group relative px-8 py-4 bg-gold-500 text-black font-bold uppercase tracking-widest hover:bg-gold-400 transition-all clip-path-slant"
            >
              <span className="flex items-center gap-2">
                Start Forging <Sparkles className="w-5 h-5" />
              </span>
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
            </Link>

            <Link
              href="/manifestos"
              className="px-8 py-4 border border-zinc-700 text-zinc-300 font-bold uppercase tracking-widest hover:border-gold-500 hover:text-gold-400 transition-colors"
            >
              Browse Designs
            </Link>
          </div>
        </div>
      </section>

      {/* Teaser Section (adapted from BSV Music Manifesto teaser) */}
      <section className="py-24 px-6 bg-zinc-900/30 border-t border-white/5">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-serif font-bold text-white mb-8">
            "This is not decline. It is dereliction."
          </h2>
          <p className="text-lg text-zinc-400 mb-12 leading-relaxed">
            We inhabit a world that treats prose like a nuisance and language like an inconvenience.
            Human Designs is the counter-culture. It is the return to intellect, structure, and sovereignty.
          </p>
          <Link
            href="/manifesto"
            className="inline-flex items-center gap-2 text-gold-400 hover:text-gold-300 transition-colors font-medium uppercase tracking-wider"
          >
            Forge Your Own <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}
