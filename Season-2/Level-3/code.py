import os
from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

# Set the absolute path to the template directory
template_dir = os.path.abspath("Season-2/Level-3/templates")
app.template_folder = template_dir

# Hard-coded planet data
planet_data = {
    "Mercury": "The smallest and fastest planet in the Solar System.",
    "Venus": "The second planet from the Sun and the hottest planet.",
    "Earth": "Our home planet and the only known celestial body to support life.",
    "Mars": "The fourth planet from the Sun and often called the 'Red Planet'.",
    "Jupiter": "The largest planet in the Solar System and known for its great red spot.",
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        planet = request.form.get("planet")

        # Check if the planet name contains potentially dangerous content
        if planet is not None and "script" in planet.lower():
            return "<h2>Blocked</h2></p>"

        # Escape the planet name to prevent XSS attacks
        sanitized_planet = escape(planet)

        if planet:
            try:
                # Validate the planet name
                normalized_planet = next((p for p in planet_data if p.lower() == planet.lower()), None)
                if normalized_planet is None:
                    return "<h2>Unknown planet.</h2>"
                return render_template(
                    "details.html", planet=sanitized_planet, info=planet_data[normalized_planet]
                )
            except Exception as e:
                return f"<h2>Error: {escape(str(e))}</h2>"
        else:
            return "<h2>Please enter a planet name.</h2>"

    return render_template("index.html")

def get_planet_info(planet):
    return planet_data.get(planet, "Unknown planet.")

if __name__ == "__main__":
    app.run()
