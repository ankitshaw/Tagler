from backend.train.nlp_trainer import NLPTagTrainer


class NLPTagClassifier():

    def load_model():
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
        path = 'saved_weights.pt'
        model.load_state_dict( torch.load( path ) )

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
            classifier  = load_model()
            data        = NLPTagTrainer.pipeline(text)
            output      = classifier(data[0].to(device), data[1].to(device))
            output      = output.detach().cpu().numpy()

        exception_type = np.argmax(output,axis=1)

        return exception_type

    def publish_result( self, result ):
        pass


    def perform_healing( self, steps ):
        pass


    def query_resolution( self, exception, exception_type ):
        pass


    def execute():
        """
        Classifies type of exception and performs the resolution steps

        Returns:
        --------
            bool - True is successful classification else false
        """
        exception_type = classify_exception( exception )
        publish_result( exception_type )
        steps = query_resolution( exception, exception_type )
        perform_healing( steps )
        pass
