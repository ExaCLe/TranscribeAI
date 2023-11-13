def log(string, canvas, canvas_log_id):
    print(string)
    canvas.itemconfig(canvas_log_id, text=string)
