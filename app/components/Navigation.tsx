"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Mascot } from "./Mascot";
import { cn } from "@/lib/utils";

export function Navigation() {
    const pathname = usePathname();

    const links = [
        { href: "/", label: "Home" },
        { href: "/manifesto", label: "Forge Design" }, // Link to create/edit page
        { href: "/manifestos", label: "Browse Designs" }, // Link to a page listing all designs
        { href: "/about", label: "About" }, // A generic "About" page, analogous to Manifesto
    ];

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black/50 backdrop-blur-xl">
            <div className="container mx-auto px-6 h-16 flex items-center justify-between">
                <Link href="/" className="flex items-center gap-3 group">
                    <Mascot className="w-8 h-8 text-gold-400 transition-transform group-hover:scale-110" />
                    <span className="font-serif font-bold text-xl tracking-tight text-gradient-gold">
                        Human Designs
                    </span>
                </Link>

                <div className="hidden md:flex items-center gap-8">
                    {links.map((link) => (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={cn(
                                "text-sm font-medium transition-colors hover:text-gold-400",
                                pathname === link.href ? "text-gold-400" : "text-zinc-400"
                            )}
                        >
                            {link.label}
                        </Link>
                    ))}
                </div>

                <div className="flex items-center gap-4">
                    <button className="px-4 py-2 text-xs font-bold uppercase tracking-wider bg-gold-500/10 text-gold-400 border border-gold-500/20 hover:bg-gold-500/20 transition-all rounded-sm">
                        Connect Wallet
                    </button>
                </div>
            </div>
        </nav>
    );
}
