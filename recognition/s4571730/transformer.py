from tensorflow.keras import layers
import tensorflow as tf 
import copy
from dense_net import dense_block

def transformer_layer(latent_size, proj_size, num_heads, num_trans_blocks, dense_layers):
    inputs_orig = layers.Input(shape=(latent_size, proj_size))

    input_plus_output = copy.deepcopy(inputs_orig)
    # Create multiple layers of the Transformer block.
    for _ in range(num_trans_blocks):
        # Layer norm
        norm = layers.LayerNormalization()(inputs_orig)
        # Create QKV self-attention layer.
        # Multihead becomes self-attetion when q = k = v. v = k if not supplied
        attention_output = layers.MultiHeadAttention(
            num_heads, proj_size)(norm, norm)

        # pass to a linear layer
        attention_output = layers.Dense(proj_size)(attention_output)

        # Add output to input
        attention_output = layers.Add()([attention_output, inputs_orig])

        # Apply layer normalization 2.
        attention_output = layers.LayerNormalization()(attention_output)

        # Dense MLP block
        output = dense_block(dense_layers)(attention_output)

        # Skip connection 2.
        input_plus_output = layers.Add()([output, attention_output])

    # Create the Keras model.
    return tf.keras.Model(inputs=inputs_orig, outputs=input_plus_output)