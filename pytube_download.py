import ffmpeg
import os


def pytube_down(yt, resolution, download_path, output_name=''):
    print(resolution)
    print(yt.watch_url)
    print(yt.title)
    print(download_path)
    if resolution == 'high':
        if resolution == 'resolution: high, 1440p, 1080p, 720p 480p ...' or resolution == '':
            print('해상도 입력이 잘못되었습니다. 가장 높은 해상도로 다운로드합니다.')
        v_path = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by(
            'resolution').desc().first().download()

    else:
        try:
            v_path = yt.streams.filter(adaptive=True, file_extension='mp4', resolution=resolution,
                                       only_video=True).order_by('resolution').desc().first().download()
        except AttributeError:
            print('\n선택한 해상도를 지원하지 않습니다.\n영상에서 지원하는 높은 해상도로 다운로드 합니다.')
            v_path = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by(
                'resolution').desc().first().download()

        except:
            print('\nURL 에러. 영상이 일부 공개, 비공개, 삭제된 영상인 지 확인해주세요.')
            print('\nDownload Failed!')
            return '다운로드 실패!'

    a_path = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by(
        "abr").desc().first().download(filename='audio.mp4')

    v = ffmpeg.input(v_path)
    a = ffmpeg.input(a_path)

    if output_name == '':
        output_name = download_path + '/' + v_path[v_path.rindex('\\')+1:]
    else:
        output_name = download_path + '/' + output_name

    print(output_name)

    ffmpeg.output(v, a, output_name, vcodec='copy', acodec='copy', loglevel='quiet').run()

    os.remove(v_path), os.remove(a_path)
    print('\nDownload Complete!\n')
    return '다운로드 완료!'
