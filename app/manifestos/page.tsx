"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Loader2, PlusCircle, Trash2, Edit } from "lucide-react";
import { cn } from "@/lib/utils";

interface Manifesto {
    id: number;
    title: string;
    author: string;
    created_at: string;
    updated_at: string;
}

export default function ManifestosPage() {
    const [manifestos, setManifestos] = useState<Manifesto[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchManifestos = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch("/api/manifestos");
            if (!response.ok) {
                throw new Error("Failed to fetch manifestos");
            }
            const data: Manifesto[] = await response.json();
            setManifestos(data);
        } catch (err: any) {
            setError(err.message || "An error occurred while fetching manifestos.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchManifestos();
    }, [fetchManifestos]);

    const handleDelete = async (id: number) => {
        if (!window.confirm("Are you sure you want to delete this manifesto?")) {
            return;
        }
        try {
            const response = await fetch(`/api/manifestos/${id}`, {
                method: "DELETE",
            });
            if (!response.ok) {
                throw new Error("Failed to delete manifesto");
            }
            fetchManifestos(); // Re-fetch the list after deletion
        } catch (err: any) {
            setError(err.message || "An error occurred while deleting manifesto.");
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-black py-24 px-6 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-gold-400" />
                <p className="ml-3 text-gold-400">Loading Designs...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-black py-24 px-6 flex flex-col items-center justify-center">
                <h1 className="text-4xl font-serif font-bold text-red-500 mb-4">Error</h1>
                <p className="text-zinc-400">{error}</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-black py-24 px-6">
            <div className="max-w-6xl mx-auto">
                <div className="flex items-end justify-between mb-12">
                    <div>
                        <h1 className="text-4xl md:text-5xl font-serif font-bold text-white mb-4">
                            Browse Designs
                        </h1>
                        <p className="text-zinc-400">
                            Explore sovereign statements from the community.
                        </p>
                    </div>
                    <div className="flex gap-2">
                        <Link href="/manifesto" className="px-4 py-2 bg-gold-500/10 text-gold-400 border border-gold-500/20 hover:bg-gold-500/20 transition-all rounded-sm flex items-center gap-2">
                            <PlusCircle className="w-4 h-4" /> Create New
                        </Link>
                    </div>
                </div>

                <div className="glass-panel rounded-xl overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="bg-white/5 text-zinc-500 text-xs uppercase tracking-wider border-b border-white/10">
                            <tr>
                                <th className="px-6 py-4 font-medium w-12">#</th>
                                <th className="px-6 py-4 font-medium">Title</th>
                                <th className="px-6 py-4 font-medium hidden md:table-cell">Author</th>
                                <th className="px-6 py-4 font-medium text-right">Created At</th>
                                <th className="px-6 py-4 font-medium w-24 text-center">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {manifestos.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="text-center py-8 text-zinc-500">
                                        No designs found. Be the first to create one!
                                    </td>
                                </tr>
                            ) : (
                                manifestos.map((manifesto, index) => (
                                    <tr
                                        key={manifesto.id}
                                        className="group hover:bg-white/5 transition-colors"
                                    >
                                        <td className="px-6 py-4 text-zinc-500 font-mono text-sm group-hover:text-white">
                                            {index + 1}
                                        </td>
                                        <td className="px-6 py-4">
                                            <Link href={`/manifesto?id=${manifesto.id}`} className="font-medium text-white group-hover:text-gold-400 transition-colors">
                                                {manifesto.title}
                                            </Link>
                                        </td>
                                        <td className="px-6 py-4 text-zinc-400 hidden md:table-cell">
                                            {manifesto.author}
                                        </td>
                                        <td className="px-6 py-4 text-zinc-500 text-right text-sm font-mono">
                                            {new Date(manifesto.created_at).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <Link href={`/manifesto?id=${manifesto.id}&edit=true`} className="p-2 hover:text-gold-400 text-zinc-400 transition-colors">
                                                    <Edit className="w-4 h-4" />
                                                </Link>
                                                <button onClick={() => handleDelete(manifesto.id)} className="p-2 hover:text-red-500 text-zinc-400 transition-colors">
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
