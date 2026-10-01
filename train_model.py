"""Optional: rebuild the saved model files from the CSV.  Run:  python train_model.py"""
import pipeline

art = pipeline.build()
pipeline.save(art)
print("Gradient Boosting test scores:", art["meta"]["gb"])
print("Saved to artifacts/")
