# AI Photo Sampler

The objective of this app is to help sampling and organizing the acquisition
of images to train AI models. It has a android app that is associated with
and can be download thought the [Google Store (soon)]().

# Usage
It is implemented using Django admin, and can be accessed using path `admin/pumpwood-auth-app/gui/`. Pumpwood is a web development framework created by Murabei, and helps to standardize the microservice communication (that is why the path...). It is possible to interact with the Photo Sampler using API, Web Interface and the App.

<p align = "center">
  ![App Schema](docs/app_schema.png?raw=true)
</p>

<figcaption align = "center">
  <b>AI Photo Sampler can be used thought api, web interface and using an Android app.</b>
</figcaption>




## API
The API can be used to register the photos that will be  at some experiment prior to the acquisition. This helps to better organize the image sampling and also add extra information that can be used at model training  (numerical e categorical). It is also possible to add dimensions to the images with a key/value JSON field to help searching the images.

The most simple way to interact with the api is using the pumpwood communication package. It abstract most of the api comunication with simple functions, bellow there is an example of how to create image registrations that can be later associated with photos using the app or web site.

```
from pumpwood_communication.microservices import PumpWoodMicroService

# Create the microservice object and login
microservice = PumpWoodMicroService(
    server_url="http://0.0.0.0:8000/",
    username="pumpwood", password="pumpwood")
microservice.login()


microservice.save({
    "model_class": "DescriptionImage",
    "description": "Big white cat 1",
    "notes": "",
    "extra_info": {
      "animal": "cat",
      "color": "white",
      "weight": 3.2
    },
    "dimentions": {
      "dataset": "animals",
    },
})

microservice.save({
    "model_class": "DescriptionImage",
    "description": "Big black cat",
    "notes": "",
    "extra_info": {
      "animal": "cat",
      "color": "black",
      "weight": 2.9
    },
    "dimentions": {
      "dataset": "animals",
    },
})

microservice.save({
    "model_class": "DescriptionImage",
    "description": "small black cat",
    "notes": "",
    "extra_info": {
      "animal": "cat",
      "color": "black",
      "weight": 0.9
    },
    "dimentions": {
      "dataset": "animals",
    },
})

microservice.save({
    "model_class": "DescriptionImage",
    "description": "small white cat",
    "notes": "",
    "extra_info": {
      "animal": "cat",
      "color": "white",
      "weight": 1.2
    },
    "dimentions": {
      "dataset": "animals",
    },
})

microservice.save({
    "model_class": "DescriptionImage",
    "description": "big black dog",
    "notes": "",
    "extra_info": {
      "animal": "dog",
      "color": "black",
      "weight": 5
    },
    "dimentions": {
      "dataset": "animals",
    },
})
```

It is also possible to list and download the images using the API. For more information on the APIs end-point consult Pumpwood Comunication documentation.

```
file_path = "app_db/"
photos_list = microservice.list_without_pag(
    "descriptionimage", filter_dict={
        "team_id": 4, "file__isnull": False})
dimentions = pd.DataFrame([x["dimentions"] for x in photos_list])
pd_photos_list = pd.DataFrame(photos_list)

for row in photos_list:
    file_name = "%s.jpeg" % row['pk']
    microservice.retrieve_file(
        model_class="DescriptionImage", pk=row['pk'],
        file_field="file", save_path=file_path, file_name=file_name,
        if_exists="overwrite")

description = json.dumps(photos_list, indent=2)
with open(file_path + "photo_description.json", "w") as file:
    file.write(description)
```

## Web Interface
The web interface is based in Django Admin using [Jet extession](https://github.com/geex-arts/django-jet) and can be acessed at `admin/pumpwood-auth-app/gui/`.

<figure>

![App Schema](docs/django_admin.png?raw=true)

<figcaption align="center">
  <b>Django Admin used to interact with AI Photo Sampler. Experiment Team,
  teams associated with an experiment sampling; Team/User association,
  associate a user with a team; Sampled image, register images and associate
  photos</b>
</figcaption>

</figure>

#### Experiment Team
An organization of the user in experiment teams. Each user can only be associated with one team. When using the app, the photos will be associated with with the user's team at the moment. It is also possible to associate key/value dimensions for teams.

<figure>

![App Schema](docs/team.png?raw=true)

<figcaption align="center">
  <b>Team edition page.</b>
</figcaption>

</figure>

#### Team/User association
Association of each user to a team. This is used to set the image team when acquiring using the mobile app, it also limit the available images to associate image taken with app (only images from user team are available).

<figure>

![App Schema](docs/team.png?raw=true)

<figcaption align="center">
  <b>Team/user edition page.</b>
</figcaption>

</figure>

#### Sampled image
Correspond to the sampled images, they can be uploaded using the API, Web and also by the mobile app. Teams information is automatically associated with the user's teams when an image entry is created.

<figure>

![App Schema](docs/photo_general.png?raw=true)

<figcaption align="center">
  <b>General information for the photo.</b>
</figcaption>

</figure>

An image can be uploaded by API, web and app. This sheet show the uploaded image and make it possible to upload one using the web interface.

<figure>

![App Schema](docs/photo_image.png?raw=true)

<figcaption align="center">
  <b>General information for the photo.</b>
</figcaption>

</figure>


It is possible to associate dimensions to the images to facilitate posterior search and also extra_info that can be used to train models.

<figure>

![App Schema](docs/photo_extra.png?raw=true)

<figcaption align="center">
  <b>Image upload and information.</b>
</figcaption>

</figure>

## APP Interface
App interface is available at the app repository.

# Testing
It is possible to test locally using docker-compose and test database docker images. Test photos were extracted from [ChesPhoto Dataset](https://arxiv.org/abs/2007.06199).

There is a bash script that helps to deploy test environment locally `test-aux/docker-compose/docker-up.bash`.

# Deploy
Kubernets is the most simple way to deploy AI Photo Sampler on cloud. It is important to map a disk to `STORAGE_LOCAL_PATH`
variable or set for google bucket or aws s3 as storage back end.

<b>Deploy using local directory:</b>
```
pumpwood-auth-app:
  image: southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/ai-photo-sampler-app:$PUMPWOOD_AUTH_APP
  environment:
    - STORAGE_TYPE=local
    - STORAGE_LOCAL_PATH=media/

  # Just for tests it is not necessary to make a volume, but changes won't
  # persist
  volumes:
    - test-media-volume:/django/media/
```

<b>Deploy using AWS S3:</b>
```
pumpwood-auth-app:
  image: southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/ai-photo-sampler-app:$PUMPWOOD_AUTH_APP
  environment:
    - STORAGE_TYPE=aws_s3
    - AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    - STORAGE_BUCKET_NAME=$STORAGE_BUCKET_NAME
```

<b>Deploy using google bucket:</b>
```
pumpwood-auth-app:
  image: southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/ai-photo-sampler-app:$PUMPWOOD_AUTH_APP
  environment:
    - STORAGE_TYPE=google_bucket
    - STORAGE_BUCKET_NAME=$STORAGE_BUCKET_NAME
    - GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/key-storage.json

    # Have to map the google credential file to the container
    volumes:
      - test-bucket-config:/etc/secrets/
```
