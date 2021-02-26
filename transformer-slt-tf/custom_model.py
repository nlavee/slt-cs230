import opennmt
import tensorflow as tf

class MyCustomTransformer(opennmt.models.Transformer):
    def __init__(self):
        super().__init__(
            source_inputter=opennmt.inputters.WordEmbedder(embedding_size=512, dropout=0.1),
            target_inputter=opennmt.inputters.WordEmbedder(embedding_size=512, dropout=0.1),
            num_layers=2,
            num_units=512,
            num_heads=8,
            ffn_inner_dim=2048,
            dropout=0.1,
            attention_dropout=0.1,
            ffn_dropout=0.1,
            ffn_activation=tf.nn.softmax,
        )

    # Here you can override any method from the Model class for a customized behavior.

model = MyCustomTransformer
