import camera
import cloud
import print

def main():
  img_path = camera.main()
  cloud.main(img_path)


if __name__ == "__main__":
    main()