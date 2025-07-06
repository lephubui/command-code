import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Card, CardContent } from "./components/ui/card";
import { BadgeCheck, Calendar, Target, BookOpen, Smile, HelpCircle, Brain, ClipboardList } from "lucide-react";

export default function CreatePlan() {
    const location = useLocation();
    const navigate = useNavigate();
    const advice = location.state?.advice;

    const [plan, setPlan] = useState(advice || ''); // Prepopulate the plan with advice

    if (!advice) {
        // Redirect to search page if no advice is provided
        navigate('/search');
        return null;
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle plan submission logic here
        console.log('Plan created:', plan);
    };

    return (
        <div className="max-w-5xl mx-auto px-6 py-10 space-y-10">
            <header className="text-center">
                <h1 className="text-4xl font-bold mb-4">🎓 StudyPlan Buddy</h1>
                <p className="text-lg text-gray-600">
                    A smart and supportive guide to help international students thrive in U.S. universities.
                </p>
            </header>

            <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <BookOpen className="text-blue-600" />
                            <h2 className="text-xl font-semibold">Understand Your Courses</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Review syllabi and assignment deadlines.</li>
                            <li>Track exam dates and key topics.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <Target className="text-green-600" />
                            <h2 className="text-xl font-semibold">Set SMART Goals</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Break long-term goals into weekly wins.</li>
                            <li>Make goals Specific, Measurable, Achievable, Relevant, and Time-bound.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <Calendar className="text-purple-600" />
                            <h2 className="text-xl font-semibold">Build a Weekly Schedule</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Block time for lectures, labs, and reviews.</li>
                            <li>Use planners or apps like Google Calendar or Notion.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <ClipboardList className="text-yellow-600" />
                            <h2 className="text-xl font-semibold">Stay Organized</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Use to-do lists, color-coded folders, and reminders.</li>
                            <li>Prioritize assignments by urgency and weight.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <Brain className="text-indigo-600" />
                            <h2 className="text-xl font-semibold">Use Campus Resources</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Find quiet zones, tutoring centers, and study groups.</li>
                            <li>Meet with academic advisors regularly.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <Smile className="text-pink-600" />
                            <h2 className="text-xl font-semibold">Stay Motivated & Care for Yourself</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Celebrate small wins, visualize success, and exercise regularly.</li>
                            <li>Sleep well, eat balanced meals, and take mindful breaks.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <HelpCircle className="text-red-600" />
                            <h2 className="text-xl font-semibold">Ask for Help</h2>
                        </div>
                        <ul className="list-disc ml-5 text-gray-700">
                            <li>Utilize office hours and peer discussions.</li>
                            <li>Reach out to counselors or international student services.</li>
                        </ul>
                    </CardContent>
                </Card>

                <Card className="md:col-span-2">
                    <CardContent className="p-6 text-center">
                        <div className="flex justify-center mb-2">
                            <BadgeCheck className="text-emerald-500" size={32} />
                        </div>
                        <h2 className="text-2xl font-bold mb-2">✅ Final Tip</h2>
                        <p className="text-gray-700">
                            Everyone studies differently. Don’t compare—customize your rhythm and adjust as needed. You’ve got this! 💪
                        </p>
                    </CardContent>
                </Card>
            </section>

            <section className="mt-10">
                <h2 className="text-2xl font-bold mb-4">Create Your Plan</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="plan">Plan:</label>
                        <textarea
                            id="plan"
                            className="form-control"
                            value={plan}
                            onChange={(e) => setPlan(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary mt-3">Save Plan</button>
                </form>
            </section>
        </div>
    );
}