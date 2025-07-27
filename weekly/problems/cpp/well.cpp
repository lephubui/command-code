#include <iostream>
#include <string>

int main() {
    std::string communityName = "PuzzleTech Wizards";
    std::string welcomeMessage = "Welcome to " + communityName + "!\n\n"
                                 "We're thrilled to have you join our community of passionate software engineers. "
                                 "Here, we dive into mind-bending coding challenges, experiment with cutting-edge technologies, "
                                 "and collaborate on innovative projects.\n\n"
                                 "Whether you're cracking algorithms, building with new frameworks, or sharing your latest hacks, "
                                 "this is your space to grow, connect, and innovate.\n\n"
                                 "Introduce yourself, share a puzzle that's stumped you, or jump into discussions. "
                                 "Let's solve, build, and push tech boundaries together!\n\n"
                                 "#PuzzleTechWizards #CodingChallenges #TechInnovation";

    std::cout << welcomeMessage << std::endl;

    return 0;
}