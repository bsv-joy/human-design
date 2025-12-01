"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState, useCallback } from "react";
import { ManifestoContent } from "../components/ManifestoContent";
import { ManifestoEditor } from "../components/ManifestoEditor";
import { Loader2 } from "lucide-react";
import Link from "next/link";

interface Manifesto {
    id: number;
    title: string;
    content: string;
    author: string;
    created_at: string;
    updated_at: string;
    // Human Design Chart Fields
    birth_datetime_utc?: string; // Stored as ISO string
    birth_latitude?: number;
    birth_longitude?: number;
    birth_timezone_str?: string;
    chart_type?: string;
    chart_strategy?: string;
    chart_inner_authority?: string;
    chart_profile?: string;
    chart_incarnation_cross?: string;
    chart_data_json?: string; // JSON string
}

export default function ManifestoPage() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const id = searchParams.get("id");
    const editMode = searchParams.get("edit") === "true";

    const [manifesto, setManifesto] = useState<Manifesto | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchManifesto = useCallback(async () => {
        if (!id) {
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`/api/manifestos/${id}`);
            if (!response.ok) {
                throw new Error("Failed to fetch manifesto");
            }
            const data: Manifesto = await response.json();
            setManifesto(data);
        } catch (err: any) {
            setError(err.message || "An error occurred while fetching.");
        } finally {
            setLoading(false);
        }
    }, [id]);

    useEffect(() => {
        fetchManifesto();
    }, [fetchManifesto]);

    const handleSave = () => {
        fetchManifesto(); // Re-fetch to display updated content
        router.push(`/manifesto?id=${id}`); // Exit edit mode
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-black py-24 px-6 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-gold-400" />
                <p className="ml-3 text-gold-400">Loading Manifesto...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-black py-24 px-6 flex flex-col items-center justify-center">
                <h1 className="text-4xl font-serif font-bold text-red-500 mb-4">Error</h1>
                <p className="text-zinc-400">{error}</p>
                <Link href="/manifesto" className="mt-6 text-gold-400 hover:underline">
                    Go back to create a new manifesto
                </Link>
            </div>
        );
    }

    if (editMode && manifesto) {
        return (
            <div className="min-h-screen bg-black py-24 px-6">
                <ManifestoEditor manifestoData={manifesto} onSave={handleSave} />
            </div>
        );
    }

    if (id && manifesto) {
        return (
            <div className="min-h-screen bg-black py-24 px-6">
                <div className="max-w-4xl mx-auto flex justify-end mb-4">
                    <Link
                        href={`/manifesto?id=${id}&edit=true`}
                        className="px-4 py-2 bg-gold-500/10 text-gold-400 border border-gold-500/20 hover:bg-gold-500/20 transition-all rounded-sm"
                    >
                        Edit Design
                    </Link>
                </div>
                <ManifestoContent
                    title={manifesto.title}
                    content={manifesto.content}
                    author={manifesto.author}
                    chart_type={manifesto.chart_type}
                    chart_strategy={manifesto.chart_strategy}
                    chart_inner_authority={manifesto.chart_inner_authority}
                    chart_profile={manifesto.chart_profile}
                    chart_incarnation_cross={manifesto.chart_incarnation_cross}
                />
            </div>
        );
    }

    // Default: Create new manifesto
    return (
        <div className="min-h-screen bg-black py-24 px-6">
            <h1 className="text-4xl md:text-5xl font-serif font-bold text-white mb-4 text-center">
                Forge Your Own Design
            </h1>
            <p className="text-zinc-400 text-center mb-8">
                Unleash your intellect and craft a new statement for the digital age.
            </p>
            <ManifestoEditor onSave={() => router.push('/manifesto')} /> {/* Redirect to home or list after create */}
        </div>
    );
}