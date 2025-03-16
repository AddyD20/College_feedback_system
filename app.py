from flask import Flask , request , jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["college_feedback"]
feedback_collection = db["feedbacks"]

@app.route("/submit_feedback" , methods= ["POST"])
def submit_feedback():
    data = request.json

    required_field = [{"student_name" , "course_name" , "rating" , "comment" , "solved_doubts" , "interactive_session" , "teaching_pace" , "clarity" , "study_material"}]
    if not all (field in data for field in required_field):
        return jsonify({"message":"Fill the missing fields"}) , 404

    feedback = {
        "student_name": data["student_name"],
        "course_name": data["course_name"],
        "rating": int(data["rating"]),
        "comment": data.get("comment" , ""),
        "solved_doubts": data["Solved_doubts"],
        "interactive_session": data["interactive_session"],
        "teaching_pace": data["teaching_pace"],
        "clearity": int(data["clarity"]),
        "study_material": int(data["study_material"])

    }

    feedback_collection.insert_one(feedback)
    return jsonify("Feedback submitted succesfully")


@app.route("/course_feedback/<course_name>", methods = ["GET"])
def get_course_feedback(course_name):
    feedbacks = list(feedback_collection.find({"course_name":course_name}, {"_id": 0}))
    if not feedbacks:
        return jsonify({"message: No feedbacks found for this course"}), 404
    return jsonify(feedbacks)

@app.route("/average_ratings/<course_name>", methods = ["GET"])
def average_course_feedback(course_name):
    feedbacks= list(feedback_collection.find({"course_name": course_name}))
    if not feedbacks:
        return jsonify({"message: No feedbacks found for this course"}),404

    avg_rating = sum(f["rating"] for f in feedbacks)/len(feedbacks)
    avg_clarity = sum(f["clarity"] for f in feedbacks)/ len(feedbacks)

    return jsonify({
        "course_name": course_name,
        "average_ratings": (avg_rating,2),
        "average_clarity": (avg_clarity,2)
    })
 

if __name__ == "__main__":
    app.run(debug=True)