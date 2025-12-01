import React from "react";

interface ManifestoContentProps {
    title: string;
    content: string;
    author: string;
    chart_type?: string;
    chart_strategy?: string;
    chart_inner_authority?: string;
    chart_profile?: string;
    chart_incarnation_cross?: string;
}

export function ManifestoContent({
    title, 
    content, 
    author, 
    chart_type, 
    chart_strategy,
    chart_inner_authority,
    chart_profile,
    chart_incarnation_cross
}: ManifestoContentProps) {
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

            {chart_type && (
                <div className="glass-panel rounded-xl p-6 mb-8">
                    <h3 className="text-2xl font-serif font-bold text-white mb-4">Human Design Chart Summary</h3>
                    <ul className="text-zinc-400 space-y-2">
                        <li><strong className="text-gold-400">Type:</strong> {chart_type}</li>
                        <li><strong className="text-gold-400">Strategy:</strong> {chart_strategy}</li>
                        <li><strong className="text-gold-400">Inner Authority:</strong> {chart_inner_authority}</li>
                        <li><strong className="text-gold-400">Profile:</strong> {chart_profile}</li>
                        <li><strong className="text-gold-400">Incarnation Cross:</strong> {chart_incarnation_cross}</li>
                    </ul>
                </div>
            )}

            <div className="text-white whitespace-pre-wrap">
                {content}
            </div>

            {/* You can add more sections here if your dynamic content will also have structured parts,
                or if you parse markdown/HTML from 'content' and render it.
                For now, we display content as plain text, respecting line breaks. */}

        </article>
    );
}