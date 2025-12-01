"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils"; // Assuming utils.ts is copied and has cn
import { ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import moment from 'moment-timezone';

interface HumanDesignChartSummary {
    type: string;
    strategy: string;
    inner_authority: string;
    profile: string;
    incarnation_cross: string;
    chart_data_json: string; // The full JSON response
}

export function ManifestoEditor({ manifestoData, onSave }: { manifestoData?: any, onSave: () => void }) {
    const [title, setTitle] = useState(manifestoData?.title || "");
    const [content, setContent] = useState(manifestoData?.content || "");
    const [author, setAuthor] = useState(manifestoData?.author || "Anonymous");

    // Human Design states
    const [birthDate, setBirthDate] = useState(manifestoData?.birth_datetime_utc ? moment.utc(manifestoData.birth_datetime_utc).format('YYYY-MM-DD') : "");
    const [birthTime, setBirthTime] = useState(manifestoData?.birth_datetime_utc ? moment.utc(manifestoData.birth_datetime_utc).format('HH:mm') : "");
    const [latitude, setLatitude] = useState<number | string>(manifestoData?.birth_latitude || "");
    const [longitude, setLongitude] = useState<number | string>(manifestoData?.birth_longitude || "");
    const [timezone, setTimezone] = useState(manifestoData?.birth_timezone_str || "UTC"); // Default to UTC

    const [isCalculatingChart, setIsCalculatingChart] = useState(false);
    const [calculatedChart, setCalculatedChart] = useState<HumanDesignChartSummary | null>(null);
    const [chartCalculationError, setChartCalculationError] = useState<string | null>(null);
    const [isHDBirthDataOpen, setIsHDBirthDataOpen] = useState(false);

    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    // Initialize calculatedChart if manifestoData already has chart details
    useEffect(() => {
        if (manifestoData && manifestoData.chart_type) {
            setCalculatedChart({
                type: manifestoData.chart_type,
                strategy: manifestoData.chart_strategy,
                inner_authority: manifestoData.chart_inner_authority,
                profile: manifestoData.chart_profile,
                incarnation_cross: manifestoData.chart_incarnation_cross,
                chart_data_json: manifestoData.chart_data_json
            });
            setIsHDBirthDataOpen(true); // Open the section if data exists
        }
    }, [manifestoData]);

    const handleCalculateChart = async () => {
        setChartCalculationError(null);
        if (!birthDate || !birthTime || !latitude || !longitude || !timezone) {
            setChartCalculationError("Please fill all birth data fields.");
            return;
        }

        const combinedDateTime = `${birthDate}T${birthTime}:00`;
        const birth_datetime_utc = moment.tz(combinedDateTime, timezone).utc().toISOString();

        setIsCalculatingChart(true);
        try {
            const response = await fetch("/api/calculate-chart", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    datetime_utc: birth_datetime_utc,
                    latitude: parseFloat(latitude as string),
                    longitude: parseFloat(longitude as string),
                    timezone_str: timezone,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to calculate Human Design chart.");
            }

            const result = await response.json();
            setCalculatedChart({
                type: result.type,
                strategy: result.strategy,
                inner_authority: result.inner_authority,
                profile: result.profile,
                incarnation_cross: result.incarnation_cross,
                chart_data_json: JSON.stringify(result) // Store the full JSON response
            });
        } catch (err: any) {
            console.error("Error calculating chart:", err);
            setChartCalculationError(err.message || "An unknown error occurred during chart calculation.");
            setCalculatedChart(null);
        } finally {
            setIsCalculatingChart(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSaving(true);
        setError(null);

        const payload: any = { title, content, author };

        // Add Human Design data to payload if calculated or present in manifestoData
        if (calculatedChart) {
            // Also include the raw birth data if a chart was calculated
            const combinedDateTime = `${birthDate}T${birthTime}:00`;
            const birth_datetime_utc = moment.tz(combinedDateTime, timezone).utc().toISOString();

            payload.birth_datetime_utc = birth_datetime_utc;
            payload.birth_latitude = parseFloat(latitude as string);
            payload.birth_longitude = parseFloat(longitude as string);
            payload.birth_timezone_str = timezone;

            payload.chart_type = calculatedChart.type;
            payload.chart_strategy = calculatedChart.strategy;
            payload.chart_inner_authority = calculatedChart.inner_authority;
            payload.chart_profile = calculatedChart.profile;
            payload.chart_incarnation_cross = calculatedChart.incarnation_cross;
            payload.chart_data_json = calculatedChart.chart_data_json;
        } else if (manifestoData && manifestoData.chart_type) {
             // If no new chart was calculated but manifestoData has existing chart info, send that
            payload.birth_datetime_utc = manifestoData.birth_datetime_utc;
            payload.birth_latitude = manifestoData.birth_latitude;
            payload.birth_longitude = manifestoData.birth_longitude;
            payload.birth_timezone_str = manifestoData.birth_timezone_str;
            payload.chart_type = manifestoData.chart_type;
            payload.chart_strategy = manifestoData.chart_strategy;
            payload.chart_inner_authority = manifestoData.chart_inner_authority;
            payload.chart_profile = manifestoData.chart_profile;
            payload.chart_incarnation_cross = manifestoData.chart_incarnation_cross;
            payload.chart_data_json = manifestoData.chart_data_json;
        }


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
                throw new Error(errorData.detail || "Failed to save design");
            }

            const result = await response.json();
            console.log("Design saved:", result);
            onSave(); // Callback to parent component
            if (!manifestoData?.id) {
                router.push(`/manifesto?id=${result.id}`); // Navigate to new manifesto
            }
        } catch (err: any) {
            console.error("Error saving design:", err);
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

                    {/* Human Design Birth Data Section */}
                    <div className="border border-white/10 rounded-lg">
                        <button
                            type="button"
                            className="w-full flex justify-between items-center p-4 bg-white/5 hover:bg-white/10 transition-colors rounded-t-lg"
                            onClick={() => setIsHDBirthDataOpen(!isHDBirthDataOpen)}
                        >
                            <span className="text-lg font-serif font-bold text-white">Human Design Birth Data (Optional)</span>
                            {isHDBirthDataOpen ? <ChevronUp className="w-5 h-5 text-gold-400" /> : <ChevronDown className="w-5 h-5 text-gold-400" />}
                        </button>
                        {isHDBirthDataOpen && (
                            <div className="p-6 border-t border-white/10 space-y-4">
                                <p className="text-zinc-400 text-sm mb-4">
                                    Enter your birth details to generate your Human Design chart.
                                </p>
                                {chartCalculationError && (
                                    <div className="bg-red-900/30 border border-red-500 text-red-300 p-4 rounded-lg mb-4">
                                        Error: {chartCalculationError}
                                    </div>
                                )}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label htmlFor="birthDate" className="block text-sm font-medium text-zinc-400 mb-2">
                                            Birth Date
                                        </label>
                                        <input
                                            type="date"
                                            id="birthDate"
                                            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                                            value={birthDate}
                                            onChange={(e) => setBirthDate(e.target.value)}
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="birthTime" className="block text-sm font-medium text-zinc-400 mb-2">
                                            Birth Time (HH:MM)
                                        </label>
                                        <input
                                            type="time"
                                            id="birthTime"
                                            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                                            value={birthTime}
                                            onChange={(e) => setBirthTime(e.target.value)}
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="latitude" className="block text-sm font-medium text-zinc-400 mb-2">
                                            Latitude
                                        </label>
                                        <input
                                            type="number"
                                            id="latitude"
                                            step="any"
                                            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                                            placeholder="e.g., 51.5074"
                                            value={latitude}
                                            onChange={(e) => setLatitude(e.target.value)}
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="longitude" className="block text-sm font-medium text-zinc-400 mb-2">
                                            Longitude
                                        </label>
                                        <input
                                            type="number"
                                            id="longitude"
                                            step="any"
                                            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                                            placeholder="e.g., -0.1278"
                                            value={longitude}
                                            onChange={(e) => setLongitude(e.target.value)}
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label htmlFor="timezone" className="block text-sm font-medium text-zinc-400 mb-2">
                                        Timezone (e.g., Europe/London)
                                    </label>
                                    <input
                                        type="text"
                                        id="timezone"
                                        className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:border-gold-500 focus:ring-1 focus:ring-gold-500 transition-colors"
                                        placeholder="e.g., Europe/London"
                                        value={timezone}
                                        onChange={(e) => setTimezone(e.target.value)}
                                    />
                                </div>
                                <button
                                    type="button"
                                    onClick={handleCalculateChart}
                                    disabled={isCalculatingChart || !birthDate || !birthTime || !latitude || !longitude || !timezone}
                                    className={cn(
                                        "w-full py-3 font-bold uppercase tracking-widest transition-all rounded-lg flex items-center justify-center gap-2",
                                        isCalculatingChart || !birthDate || !birthTime || !latitude || !longitude || !timezone
                                            ? "bg-zinc-800 text-zinc-500 cursor-not-allowed"
                                            : "bg-electric-500 text-black hover:bg-electric-400"
                                    )}
                                >
                                    {isCalculatingChart ? (
                                        <>
                                            <Loader2 className="w-5 h-5 animate-spin" /> Calculating...
                                        </>
                                    ) : (
                                        "Calculate Human Design Chart"
                                    )}
                                </button>

                                {calculatedChart && (
                                    <div className="glass-panel rounded-lg p-4 mt-6">
                                        <h3 className="text-xl font-serif font-bold text-white mb-3">Calculated Chart Summary</h3>
                                        <ul className="text-zinc-400 space-y-1 text-sm">
                                            <li><strong className="text-gold-400">Type:</strong> {calculatedChart.type}</li>
                                            <li><strong className="text-gold-400">Strategy:</strong> {calculatedChart.strategy}</li>
                                            <li><strong className="text-gold-400">Inner Authority:</strong> {calculatedChart.inner_authority}</li>
                                            <li><strong className="text-gold-400">Profile:</strong> {calculatedChart.profile}</li>
                                            <li><strong className="text-gold-400">Incarnation Cross:</strong> {calculatedChart.incarnation_cross}</li>
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}
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