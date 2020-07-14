# Databricks notebook source
#Author: Ben Tennant

# COMMAND ----------

import pyspark.sql.functions as f
from pyspark.sql.types import StructType, StructField, LongType,StringType, DoubleType
from pyspark.ml.feature import StringIndexer, Bucketizer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
sc = spark.sparkContext

# COMMAND ----------

#The data set contains information on 
snSchema = StructType([ \
                      StructField('User ID',LongType(),True), \
                      StructField('gender', StringType(),True), \
                      StructField('age',LongType(),True), \
                      StructField('salary',LongType(),True), \
                      StructField('purchased',StringType(),True)])

# COMMAND ----------

snDF = spark.read.format('csv').option('header',True).schema(snSchema).option('ignoreLeadingWhiteSpace',True).option('mode','dropMalformed').load('FileStore/tables/Social_Network_Ads.csv')

rawTrain, rawTest = snDF.randomSplit([0.75, 0.25], seed=12345)

rawTest = rawTest.repartition(20)
rawTest.write.format('csv').option('header',True).mode('overwrite').save('FileStore/tables/snTEST.csv')

# COMMAND ----------

genderIndex = StringIndexer(inputCol = 'gender',outputCol='genderIndex')

ageSplits = [-float('inf'),20,30,50,60,70,float('inf')]
ageBucketizer = Bucketizer(splits=ageSplits,inputCol='age',outputCol='ageBucket')

salarySplits = [-float('inf'),20000,40000,60000,80000,100000,120000,float('inf')]

salaryBucketizer = Bucketizer(splits=salarySplits,inputCol='salary',outputCol='salaryBucket')

purchasedIndex = StringIndexer(inputCol='purchased',outputCol='label')

vecAssem = VectorAssembler(inputCols=['genderIndex','ageBucket','salaryBucket'],outputCol='features')

dt = DecisionTreeClassifier(labelCol="label", featuresCol="features")

myStages = [genderIndex,ageBucketizer,salaryBucketizer,purchasedIndex,vecAssem,dt]

pl = Pipeline(stages=myStages)

plmodel = pl.fit(rawTrain)

# COMMAND ----------

testStream = spark.readStream.format('csv').option('header',True).schema(snSchema).option('maxFilesPerTrigger',1).load('dbfs:///FileStore/tables/snTEST.csv')

preds = plmodel.transform(testStream).select(f.col('User ID'),f.col('features'),f.col('prediction'))

query = preds.writeStream.outputMode('update').format('memory').queryName('snPreds').trigger(processingTime='15 seconds').start()

# COMMAND ----------

spark.sql("select * from snPreds").show()

# COMMAND ----------


