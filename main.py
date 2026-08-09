from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from . import crud, models, schemas
import os


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title='Business DNA Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def startup_event():
    init_db()


@app.get('/health')
def health():
    return {"status": "ok"}


@app.get('/products')
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.get('/products/{product_id}')
def retrieve_product(product_id: int, db: Session = Depends(get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail='Product not found')
    return p


@app.post('/products')
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product.dict())


@app.put('/products/{product_id}')
def put_product(product_id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    p = crud.update_product(db, product_id, data.dict())
    if not p:
        raise HTTPException(status_code=404, detail='Product not found')
    return p


@app.delete('/products/{product_id}')
def del_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Product not found')
    return {"ok": True}


@app.post('/sales')
def post_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    try:
        s = crud.create_sale(db, sale.product_id, sale.quantity)
        return {"ok": True}
    except ValueError:
        raise HTTPException(status_code=404, detail='Product not found')


@app.get('/dashboard')
def dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard(db)


@app.get('/recommendations')
def recommendations(db: Session = Depends(get_db)):
    return crud.get_recommendations(db)


@app.post('/ask-ai')
def ask_ai(payload: dict, db: Session = Depends(get_db)):
    # Simple, transparent AI stub: return a short answer with reason from business data
    question = payload.get('question')
    if not question:
        raise HTTPException(status_code=400, detail='question is required')
    # For demo, map a few sample questions
    q = question.lower()
    if 'restock' in q:
        recs = crud.get_recommendations(db)
        if recs:
            top = recs[0]
            answer = f"{top['title']}. You have { (lambda pid: next((p.current_stock for p in db.query(models.Product).filter(models.Product.id==pid)), 'few'))(top['productId']) } left."
        else:
            answer = 'No immediate restock needed.'
    elif 'most money' in q or 'most profit' in q:
        d = crud.get_dashboard(db)
        answer = d.get('best_product', {}).get('name', 'No data')
    else:
        answer = 'Try asking which product to restock or which product makes you the most money.'
    return {"answer": answer}


@app.get('/report')
def report(db: Session = Depends(get_db)):
    return crud.get_report(db)


@app.post('/sample-data')
def sample_data(db: Session = Depends(get_db)):
    crud.seed_sample_data(db)
    return {"ok": True}
