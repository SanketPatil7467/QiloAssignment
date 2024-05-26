from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pymongo import MongoClient
from bson.objectid import ObjectId

    
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")


'''
Blog Database contains blogs history such as:
Blog Name, Blog Author, Number of Likes, Number of Dislikes and Blog Content
'''
db = client["blogContent"]
blog_collection = db["blogDetails"]

'''
Comment Database contains comment history such as:
Comment containt and Refered to which Blog
'''
comment_db = client["CommentContent"]
comment_collection = comment_db["commentCollection"]

'''
Blogger Database contains blogger's detail such as:
Blogger Name, Username and Password
'''
blogger_db = client["BloggerDetails"]
blogger_collection = blogger_db["bloggerCollection"]



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    '''
    This is a home url which displays all the written blogs
    i.e : All blogs from database
    '''
    blogs = list(blog_collection.find({}, {"_id": 1, "blogName": 1,
                 "blogAuthor": 1, "likes": 1, "dislikes": 1, "content": 1}))
    return templates.TemplateResponse("home.html", {"request": request, "blogs": blogs})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    '''
    This renders up a register page for non registered users.
    Registration is compulsory to post a blog.
    '''
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/verify_blogger")
async def verify_blogger(request: Request, login_username: str = Form(...), login_password: str = Form(...)):
    '''
    Validates a user by checking username and password from
    Blogger's Database. If it is valid user then user will redirected to
    personal portfolio which contains all published blogs.
    '''
    blogger = blogger_collection.find_one(
        {"username": login_username, "password": login_password})
    if blogger:
        blogs = list(blog_collection.find({"blogAuthor": blogger["name"]}, {
                     "_id": 1, "blogName": 1, "blogAuthor": 1, "likes": 1, "dislikes": 1, "content": 1}))
        return templates.TemplateResponse("personal_account.html", {"request": request, "blogs": blogs, "blogger": blogger["name"]})
    else:
        return RedirectResponse(url="/", status_code=303)


@app.post("/{blog_id}/delete")
async def deleteBlog(request: Request, blog_id =str):
    '''
    User will use this to delete a published blog.
    '''
    blog_id = ObjectId(blog_id)
    blog_details = blog_collection.find_one({"_id" : blog_id})
    # print(blog_details)
    name = blog_details["blogAuthor"]
    blog_collection.delete_one({"_id":blog_id})
    blogs = list(blog_collection.find({"blogAuthor": name}, {
        "_id": 1, "blogName": 1, "blogAuthor": 1, "likes": 1, "dislikes": 1, "content": 1}))
    
    comments = list(comment_collection.find({}, {
        "_id": 1, "blogid": 1, "comment": 1}))
    
    return templates.TemplateResponse("personal_account.html", {"request": request, "blogs": blogs, "blogger": name})
    # return RedirectResponse(url="/", status_code=303)


@app.post("/{blog_id}/modify")
async def modifyBlogWindow(request: Request, blog_id=str):
    blog_id = ObjectId(blog_id)
    blog_details = blog_collection.find_one({"_id": blog_id})
    name = blog_details["blogAuthor"]
    return templates.TemplateResponse("modify.html", {"request": request, "blogs": blog_details, "blogger": name})


@app.post("/{blogger_name}/publish")
async def publishMyBlog(request: Request, blogger_name: str, newblogname: str = Form(...), newblogcontent: str = Form(...)):
    '''
    Validate user can add content to create new Blog using this function.
    '''
    blog_collection.insert_one({"blogName": newblogname, "blogAuthor": blogger_name,
                               "likes": 0, "dislikes": 0, "content": newblogcontent})
    blogs = list(blog_collection.find({"blogAuthor": blogger_name}, {
        "_id": 1, "blogName": 1, "blogAuthor": 1, "likes": 1, "dislikes": 1, "content": 1}))
    return templates.TemplateResponse("personal_account.html", {"request": request, "blogs": blogs, "blogger": blogger_name})


@app.post("/{blogger_name}/publish_new_blog")
async def publishNewBlog(request: Request, blogger_name: str):
    '''
    Validate user can publish new Blogs using this function.
    '''
    return templates.TemplateResponse("publish_blog.html", {"request": request, "blogger_name": blogger_name})

@app.post("/{blog_id}/{blogger}/modify_publish")
async def publishMyBlog(request: Request, blog_id: str, blogger : str, modifiedblogname: str = Form(...), modifiedblogcontent: str = Form(...)):
    '''
    Validate user can modify their published blog using this function
    '''
    prev = {"_id": blog_id}
    nextt = {"$set": {"blogName": modifiedblogname , "content":modifiedblogcontent}}
    blog_collection.update_one(prev, nextt)

    blogs = list(blog_collection.find({"blogAuthor": blogger}, {
        "_id": 1, "blogName": 1, "blogAuthor": 1, "likes": 1, "dislikes": 1, "content": 1}))
    return templates.TemplateResponse("personal_account.html", {"request": request, "blogs": blogs, "blogger": blogger})


@app.get("/update_likes/{blog_id}/{action}")
async def update_likes_get(blog_id: str, action: str):
    return RedirectResponse(url=f"/update_likes/{blog_id}/{action}", status_code=303)


@app.post("/update_likes/{blog_id}/{action}")
async def update_likes_post(blog_id: str, action: str, request: Request):
    '''
    All likes and dislikes are tracked using this function.
    '''
    blog_id = ObjectId(blog_id)
    if action == "like":
        blog_collection.update_one({"_id": blog_id}, {"$inc": {"likes": 1}})
    elif action == "dislike":
        blog_collection.update_one({"_id": blog_id}, {"$inc": {"dislikes": 1}})
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    blogs = list(blog_collection.find({}, {"_id": 1, "blogName": 1,
                 "blogAuthor": 1, "likes": 1, "dislikes": 1, "content": 1}))
    return templates.TemplateResponse("home.html", {"request": request, "blogs": blogs})


@app.post("/submit/{blog_id}")
async def submit_text(blog_id: str, commenttext: str = Form(...)):
    '''
    Add blog comments to the respected blog in comment database 
    '''
    blog_id = ObjectId(blog_id)
    comment_collection.insert_one(
        {"blogid": blog_id, "comment": commenttext})
    print(f"Submitted text: {commenttext}")
    return RedirectResponse(url="/", status_code=303)


@app.post("/add_new_blogger")
async def addNewBlogger(fullName: str = Form(...), username: str = Form(...), password: str = Form(...)):
    '''
    Create new Blogging accounts.
    '''
    blogger_collection.insert_one(
        {"name": fullName, "username": username, "password":password})
    print(f"Submitted text: {fullName}")
    return RedirectResponse(url="/", status_code=303)


@app.get("/get_login_form", response_class=HTMLResponse)
async def getLoginForm(request: Request):
    '''
    Renders Login form to validate user.
    '''
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5050)
