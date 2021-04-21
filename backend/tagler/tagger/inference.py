from tagler.poller.file import FilePoller


EXCEPT_MAPPING = { '0' : 'SYSTEM EXCEPTION', '1' : 'BUSINESS EXCEPTION' }

class NLPTagClassifier():

    def __init__( self, modelPath =  'saved_weights.pt' ):
        self.modelPath = modelPath
        self.classifier  = self.load_model()

    def load_model( self ):
        """
            Loading already trained model for Tag Classification

            Returns:
            --------
            classifier model for tagging
        """

        # import BERT-base pretrained model
        bert = AutoModel.from_pretrained('bert-base-uncased')

        # pass the pre-trained BERT to our define architecture
        model = BERT_Arch( bert )

        #load weights of best model
        model.load_state_dict( torch.load( self.modelPath ) )

        return model


    def classify_exception( self, exception ):
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
            
            data        = NLPTagTrainer.pipeline( exception )
            output      = self.classifier( data[0].to(device), data[1].to(device) )
            output      = output.detach().cpu().numpy()

        exception_type = np.argmax( output, axis = 1 )

        return exception_type




if __name__ == '__main__':
    execute('exception')
