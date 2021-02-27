python3.7 code/augment_aslg.py --input data/phoenix2014T.train.gloss --inputLabel data/phoenix2014T.train.de --output augmented_data/phoenix2014T.train.gloss.rs_10 --outputLabel augmented_data/phoenix2014T.train.de.rs_10  --num_aug=16 --alpha_sr=0.0 --alpha_rd=0.0 --alpha_ri=0.0 --alpha_rs=0.1

python3.7 code/augment_aslg.py --input data/phoenix2014T.train.gloss --inputLabel data/phoenix2014T.train.de --output augmented_data/phoenix2014T.train.gloss.rs_15 --outputLabel augmented_data/phoenix2014T.train.de.rs_15  --num_aug=16 --alpha_sr=0.0 --alpha_rd=0.0 --alpha_ri=0.0 --alpha_rs=0.15

python3.7 code/augment_aslg.py --input data/phoenix2014T.train.gloss --inputLabel data/phoenix2014T.train.de --output augmented_data/phoenix2014T.train.gloss.rs_20 --outputLabel augmented_data/phoenix2014T.train.de.rs_20  --num_aug=16 --alpha_sr=0.0 --alpha_rd=0.0 --alpha_ri=0.0 --alpha_rs=0.2

python3.7 code/augment_aslg.py --input data/phoenix2014T.train.gloss --inputLabel data/phoenix2014T.train.de --output augmented_data/phoenix2014T.train.gloss.rd_10 --outputLabel augmented_data/phoenix2014T.train.de.rd_10  --num_aug=16 --alpha_sr=0.0 --alpha_rd=0.1 --alpha_ri=0.0 --alpha_rs=0.0

python3.7 code/augment_aslg.py --input data/phoenix2014T.train.gloss --inputLabel data/phoenix2014T.train.de --output augmented_data/phoenix2014T.train.gloss.rd_15 --outputLabel augmented_data/phoenix2014T.train.de.rd_15  --num_aug=16 --alpha_sr=0.0 --alpha_rd=0.15 --alpha_ri=0.0 --alpha_rs=0.0

python3.7 code/augment_aslg.py --input data/phoenix2014T.train.gloss --inputLabel data/phoenix2014T.train.de --output augmented_data/phoenix2014T.train.gloss.rd_20 --outputLabel augmented_data/phoenix2014T.train.de.rd_20  --num_aug=16 --alpha_sr=0.0 --alpha_rd=0.2 --alpha_ri=0.0 --alpha_rs=0.0
