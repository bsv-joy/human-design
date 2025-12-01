import React from "react";

interface ManifestoContentProps {
    title: string;
    content: string;
    author: string;
}

export function ManifestoContent({ title, content, author }: ManifestoContentProps) {
    return (
        <article className="prose prose-invert prose-lg max-w-4xl mx-auto font-serif">
            <div className="mb-12 text-center border-b border-white/10 pb-12">
                <h1 className="text-4xl md:text-6xl font-bold mb-6 text-gradient-gold tracking-tight">
                    {title}
                </h1>
                <p className="text-xl text-zinc-400 mb-8 italic">
                    By {author}
                </p>
                {/* Removed KEYWORDS for dynamic content, can be re-added as a prop if needed */}
            </div>

            <div className="text-white whitespace-pre-wrap">
                {content}
            </div>

            {/* You can add more sections here if your dynamic content will also have structured parts,
                or if you parse markdown/HTML from 'content' and render it.
                For now, we display content as plain text, respecting line breaks. */}

        </article>
    );
}
