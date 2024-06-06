from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId
import zipfile

app = Flask(__name__)




if __name__ == '__main__':
    app.run()
