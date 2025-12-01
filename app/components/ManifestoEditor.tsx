"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils"; // Assuming utils.ts is copied and has cn

export function ManifestoEditor({ manifestoData, onSave }: { manifestoData?: any, onSave: () => void }) {
    const [title, setTitle] = useState(manifestoData?.title || "");
    const [content, setContent] = useState(manifestoData?.content || "");
    const [author, setAuthor] = useState(manifestoData?.author || "Anonymous");
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSaving(true);
        setError(null);

        const payload = { title, content, author };
        const method = manifestoData?.id ? "PATCH" : "POST";
        const url = manifestoData?.id ? `/api/manifestos/${manifestoData.id}` : "/api/generate-design"; // /api/generate-design maps to POST /generate-design

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to save manifesto");
            }

            const result = await response.json();
            console.log("Manifesto saved:", result);
            onSave(); // Callback to parent component
            if (!manifestoData?.id) {
                router.push(`/manifesto/${result.id}`); // Navigate to new manifesto
            }
        } catch (err: any) {
            console.error("Error saving manifesto:", err);
            setError(err.message || "An unknown error occurred.");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-6">
            <form onSubmit={handleSubmit} className="glass-panel rounded-xl p-8 mb-8">
                <h2 className="text-2xl font-serif font-bold mb-6 text-white flex items-center gap-2">
                    {manifestoData?.id ? "Edit Your Design" : "Create a New Design"}
                </h2>

                {error && (
                    <div className="bg-red-900/30 border border-red-500 text-red-300 p-4 rounded-lg mb-4">
                        Error: {error}
                    </div>
                )}

                <div className="space-y-6">
                    <div>
                        <label htmlFor="title" className="block text-sm font-medium text-zinc-400 mb-2">
                            Title
                        </label>
                        <input
                            type="text"
                            id="title"
                            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                            placeholder="A title for your sovereign design"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="content" className="block text-sm font-medium text-zinc-400 mb-2">
                            Content
                        </label>
                        <textarea
                            id="content"
                            className="w-full h-64 bg-black/50 border border-white/10 rounded-lg p-4 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors resize-y"
                            placeholder="Unleash your thoughts, craft your manifesto..."
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="author" className="block text-sm font-medium text-zinc-400 mb-2">
                            Author
                        </label>
                        <input
                            type="text"
                            id="author"
                            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                            placeholder="Your name or pseudonym"
                            value={author}
                            onChange={(e) => setAuthor(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={isSaving || !title || !content}
                        className={cn(
                            "w-full py-4 font-bold uppercase tracking-widest transition-all rounded-lg flex items-center justify-center gap-2",
                            isSaving || !title || !content
                                ? "bg-zinc-800 text-zinc-500 cursor-not-allowed"
                                : "bg-gold-500 text-black hover:bg-gold-400"
                        )}
                    >
                        {isSaving ? (
                            <>
                                Saving...
                            </>
                        ) : (
                            <>
                                {manifestoData?.id ? "Update Design" : "Publish Design"}
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}
