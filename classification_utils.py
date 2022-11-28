import tensorflow as tf
#function to discretize the variables
#input: the dataset and the list of variables' names to discretize
def discretize_data(dataset, variables):
    for variable in variables:
        #get the unique variable's values
        var = sorted(dataset[variable].unique())
        
        #generate a mapping from the variable's values to the number representation  
        mapping = dict(zip(var, range(0, len(var) + 1)))

        #add a new colum with the number representation of the variable
        dataset[variable+'_num'] = dataset[variable].map(mapping).astype(int)
    return dataset

def print_training_stats(history):
    import matplotlib.pyplot as plt
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    fig1, ax1 = plt.subplots()
    ax1.plot(epochs, loss, 'y', label='Training Loss')
    ax1.plot(epochs, val_loss, 'g', label='Validation Loss')
    ax1.plot(epochs, acc, 'r', label='Training Acc')
    ax1.plot(epochs, val_acc, 'b', label='Validation Acc')
    ax1.set_title('Training and validation Loss and Accuracy')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('')
    ax1.legend()
    
def large_model_example(
    feature_matrix_tr,
    target_array_tr,
    feature_matrix_vl,
    target_array_vl
    ):
    in_layer = tf.keras.layers.Normalization(axis=-1)
    in_layer.adapt(feature_matrix_tr)

    model = tf.keras.models.Sequential([
    in_layer,
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'), 
    tf.keras.layers.Dense(1, activation='sigmoid')
    ])


    model.compile(optimizer="adam",
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=["accuracy"]
    )

    history = model.fit(
    feature_matrix_tr,
    target_array_tr,
    batch_size=1024,
    epochs=200,
    validation_data=(feature_matrix_vl, target_array_vl),
    shuffle=True, 
    verbose=False
    )

    print_training_stats(history=history)