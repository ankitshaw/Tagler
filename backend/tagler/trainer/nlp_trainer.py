import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import transformers
from transformers import AutoModel, BertTokenizerFast

class NLPTagTrainer():

    def load_training_data():
        filePath  = "../input/logdata/train.csv"
        trainData = pd.read_csv( filePath )
        trainData = trainData.rename( columns = { "Exception (input)":"text", "Exception Category (ouput)":"label" } )
        trainData = trainData.replace( "Business Exception", 0 ).replace( "System Exception", 1 )
        return trainData

    def save_model():
        filePath = ''
        pass

    @classmethod
    def load_model():
        pass

    def tokenize_data( self, train_text, val_text, test_text ):

        # Load the BERT tokenizer
        tokenizer = _load_BERT_Tokeniser()

        # tokenize and encode sequences in the training set
        tokens_train = tokenizer.batch_encode_plus(
            train_text.tolist(),
            max_length = max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False
        )

        # tokenize and encode sequences in the validation set
        tokens_val = tokenizer.batch_encode_plus(
            val_text.tolist(),
            max_length = max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False
        )

        # tokenize and encode sequences in the test set
        tokens_test = tokenizer.batch_encode_plus(
            test_text.tolist(),
            max_length = max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False
        )

        return tokens_train, tokens_val, tokens_test


    def preprocess_data():
        data = load_training_data()
        train_text, temp_text, train_labels, temp_labels = train_test_split(data['text'], data['label'],
                                                                    random_state=2018,
                                                                    test_size=0.1,
                                                                    stratify=data['label'])

        # we will use temp_text and temp_labels to create validation and test set
        val_text, test_text, val_labels, test_labels = train_test_split(temp_text, temp_labels,
                                                                        random_state=2018,
                                                                        test_size=0.5,
                                                                        stratify=temp_labels)

        train_text, val_text, test_text  =  tokenize_data( self, train_text, val_text, test_text )

        # for train set
        train_seq  = torch.tensor(tokens_train['input_ids'])
        train_mask = torch.tensor(tokens_train['attention_mask'])
        train_y    = torch.tensor(train_labels.tolist())

        # for validation set
        val_seq = torch.tensor(tokens_val['input_ids'])
        val_mask = torch.tensor(tokens_val['attention_mask'])
        val_y = torch.tensor(val_labels.tolist())

        # for test set
        test_seq = torch.tensor(tokens_test['input_ids'])
        test_mask = torch.tensor(tokens_test['attention_mask'])
        test_y = torch.tensor(test_labels.tolist())


        return ( ( train_seq, train_mask, train_y ), ( val_seq, val_mask, val_y ), ( test_seq, test_mask, test_y ) )



    def load_BERT_Tokeniser():
        # Load the BERT tokenizer
        return BertTokenizerFast.from_pretrained('bert-base-uncased')


    def execute_training( self ):

        # import BERT-base pretrained model
        bert = AutoModel.from_pretrained('bert-base-uncased')

        ( train_seq, train_mask, train_y ), ( val_seq, val_mask, val_y ), ( test_seq, test_mask, test_y ) = preprocess_data()

        from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

        #define a batch size
        batch_size = 32

        # wrap tensors
        train_data = TensorDataset( train_seq, train_mask, train_y )

        # sampler for sampling the data during training
        train_sampler = RandomSampler( train_data )

        # dataLoader for train set
        train_dataloader = DataLoader( train_data, sampler = train_sampler, batch_size = batch_size )

        # wrap tensors
        val_data = TensorDataset( val_seq, val_mask, val_y )

        # sampler for sampling the data during training
        val_sampler = SequentialSampler( val_data )

        # dataLoader for validation set
        val_dataloader = DataLoader( val_data, sampler = val_sampler, batch_size = batch_size )

        # freeze all the parameters
        for param in bert.parameters():
            param.requires_grad = False


        # pass the pre-trained BERT to our define architecture
        model = BERT_Arch(bert)

        # push the model to GPU
        model = model.to(device)

        # optimizer from hugging face transformers
        from transformers import AdamW

        # define the optimizer
        optimizer = AdamW(model.parameters(), lr = 1e-3)

        from sklearn.utils.class_weight import compute_class_weight

        #compute the class weights
        class_wts = compute_class_weight('balanced', np.unique(train_labels), train_labels)

        # convert class weights to tensor
        weights= torch.tensor(class_wts,dtype=torch.float)
        weights = weights.to(device)

        # loss function
        cross_entropy  = nn.NLLLoss(weight=weights)

        # number of training epochs
        epochs = 30

        # set initial loss to infinite
        best_valid_loss = float('inf')

        # empty lists to store training and validation loss of each epoch
        train_losses=[]
        valid_losses=[]

        #for each epoch
        for epoch in range(epochs):

            print('\n Epoch {:} / {:}'.format(epoch + 1, epochs))

            #train model
            train_loss, _ = train()

            #evaluate model
            valid_loss, _ = evaluate()

            #save the best model
            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                torch.save(model.state_dict(), 'saved_weights.pt')

            # append training and validation loss
            train_losses.append(train_loss)
            valid_losses.append(valid_loss)

            print(f'\nTraining Loss: {train_loss:.3f}')
            print(f'Validation Loss: {valid_loss:.3f}')

        #load weights of best model
        path = 'saved_weights.pt'
        model.load_state_dict(torch.load(path))




    # function to train the model
    def train_model():

      model.train()

      total_loss, total_accuracy = 0, 0

      # empty list to save model predictions
      total_preds=[]

      # iterate over batches
      for step,batch in enumerate(train_dataloader):

        # progress update after every 50 batches.
        if step % 50 == 0 and not step == 0:
          print('  Batch {:>5,}  of  {:>5,}.'.format(step, len(train_dataloader)))

        # push the batch to gpu
        batch = [r.to(device) for r in batch]

        sent_id, mask, labels = batch

        # clear previously calculated gradients
        model.zero_grad()

        # get model predictions for the current batch
        preds = model(sent_id, mask)

        # compute the loss between actual and predicted values
        loss = cross_entropy(preds, labels)

        # add on to the total loss
        total_loss = total_loss + loss.item()

        # backward pass to calculate the gradients
        loss.backward()

        # clip the the gradients to 1.0. It helps in preventing the exploding gradient problem
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        # update parameters
        optimizer.step()

        # model predictions are stored on GPU. So, push it to CPU
        preds=preds.detach().cpu().numpy()

        # append the model predictions
        total_preds.append(preds)

      # compute the training loss of the epoch
      avg_loss = total_loss / len(train_dataloader)

      # predictions are in the form of (no. of batches, size of batch, no. of classes).
      # reshape the predictions in form of (number of samples, no. of classes)
      total_preds  = np.concatenate(total_preds, axis=0)

      #returns the loss and predictions
      return avg_loss, total_preds


    # function for evaluating the model
    def evaluate():

      print("\nEvaluating...")

      # deactivate dropout layers
      model.eval()

      total_loss, total_accuracy = 0, 0

      # empty list to save the model predictions
      total_preds = []

      # iterate over batches
      for step,batch in enumerate(val_dataloader):

        # Progress update every 50 batches.
        if step % 50 == 0 and not step == 0:

          # Calculate elapsed time in minutes.
          elapsed = format_time(time.time() - t0)

          # Report progress.
          print('  Batch {:>5,}  of  {:>5,}.'.format(step, len(val_dataloader)))

        # push the batch to gpu
        batch = [t.to(device) for t in batch]

        sent_id, mask, labels = batch

        # deactivate autograd
        with torch.no_grad():

          # model predictions
          preds = model(sent_id, mask)

          # compute the validation loss between actual and predicted values
          loss = cross_entropy(preds,labels)

          total_loss = total_loss + loss.item()

          preds = preds.detach().cpu().numpy()

          total_preds.append(preds)

      # compute the validation loss of the epoch
      avg_loss = total_loss / len(val_dataloader)

      # reshape the predictions in form of (number of samples, no. of classes)
      total_preds  = np.concatenate(total_preds, axis=0)

      return avg_loss, total_preds

    @classmethod
    def pipeline( cls, text ):
        tokenizer = _load_BERT_Tokeniser()
        token = tokenizer.batch_encode_plus(
                [text],
                max_length = max_seq_len,
                pad_to_max_length=True,
                truncation=True,
                return_token_type_ids=False
                )
        new_seq  = torch.tensor(token['input_ids'])
        new_mask = torch.tensor(token['attention_mask'])
        return [new_seq, new_mask]


    def predict( self, text ):
        with torch.no_grad():
            data = NLPTagTrainer.pipeline(text)
            output = self.model(data[0].to(device), data[1].to(device))
            output = output.detach().cpu().numpy()
            return np.argmax(output,axis=1)



class BERT_Arch(nn.Module):

    def __init__(self, bert):

      super(BERT_Arch, self).__init__()

      self.bert = bert

      # dropout layer
      self.dropout = nn.Dropout(0.1)

      # relu activation function
      self.relu =  nn.ReLU()

      # dense layer 1
      self.fc1 = nn.Linear(768,512)

      # dense layer 2 (Output layer)
      self.fc2 = nn.Linear(512,2)

      #softmax activation function
      self.softmax = nn.LogSoftmax(dim=1)

    #define the forward pass
    def forward(self, sent_id, mask):

      #pass the inputs to the model
      _, cls_hs = self.bert(sent_id, attention_mask=mask)

      x = self.fc1(cls_hs)

      x = self.relu(x)

      x = self.dropout(x)

      # output layer
      x = self.fc2(x)

      # apply softmax activation
      x = self.softmax(x)

      return x
