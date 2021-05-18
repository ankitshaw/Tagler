from typing import List
from tagler.trainer.bert import BERT_Arch
from transformers import AutoModel, BertTokenizerFast
import torch
import numpy as np

EXCEPT_MAPPING = { 0 : 'Business Exception', 1 : 'System Exception' }
class NLPTagClassifier():

    def __init__( self, modelDir:str=None, device:str="cpu"):
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.max_seq_len = 25
        self.modelDir = modelDir if modelDir else 'bert-base-uncased'
        self.classifier, self.tokenizer  = self.load_model()
        #self.tags = tags  #pass this also later
        

    def load_model( self ):
        """
            Loading already trained model for Tag Classification

            Returns:
            --------
            classifier model for tagging
        """

        tokenizer = BertTokenizerFast.from_pretrained(self.modelDir)

        # import BERT-base pretrained model
        bert = AutoModel.from_pretrained(self.modelDir)

        # pass the pre-trained BERT to our define architecture
        model = BERT_Arch( bert )
        model.to(self.device)

        #load weights of best model
        tl = torch.load( self.modelDir+"/saved_weights.pt", map_location=self.device)
        model.load_state_dict( tl )

        return model, tokenizer


    def classify_exception( self, exception ) -> str:
        """
            Classifies excpetion type based on the input text using the NLP trained model.

            Parameters:
            ----------
            exception :
                str - Exception to be classified

            Returns:
            --------
                str - Type of exception
        """

        with torch.no_grad():
            
            data        = self.pipeline( exception )
            output      = self.classifier( data[0].to(self.device), data[1].to(self.device) )
            output      = output.detach().cpu().numpy()

        print(output)
        exception_type = np.argmax( output, axis = 1 )

        return EXCEPT_MAPPING[exception_type[0]] #will have to return before argmax as raw output to check the degree of confidence else dont tag
    
    def pipeline(self, text):
        token = self.tokenizer.batch_encode_plus(
                [text],
                max_length = self.max_seq_len,
                pad_to_max_length=True,
                truncation=True,
                return_token_type_ids=False
                )
        new_seq = torch.tensor(token['input_ids'])
        new_mask = torch.tensor(token['attention_mask'])
        return [new_seq, new_mask]
