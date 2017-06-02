#Use this code after scaling the features

from sklearn.decomposition import PCA

pca = PCA(n_components = 2)

pca.fit(scaled_features_df.drop('RESULT', axis = 1))

pca_features_df = pca.transform(scaled_features_df.drop('RESULT', axis = 1))

scaled_features_df.shape

pca_features_df.shape

pca_features_pddf = pd.DataFrame(pca_features_df, index = ml_matches_df.index)

pca_features_pddf.head(1)

pca_features_pddf['RESULT'] = ml_matches_df['RESULT']