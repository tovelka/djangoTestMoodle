from django.shortcuts import render
from django.http import JsonResponse
from messenger.views import menu
from apihandler.models import Events
from django.views.decorators.csrf import csrf_exempt
import json

from django.utils import timezone
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

def parse_and_validate_datetime(date_str, field_name='purposed_datetime'):
    """
    Преобразует строку в datetime и проверяет, что дата не в прошлом.
    Возвращает объект datetime или выбрасывает ValidationError.
    """
    if not date_str:
        raise ValidationError(f"{field_name} is required.")

    # Попытка распарсить строку (ожидается ISO формат: YYYY-MM-DDTHH:MM:SS)
    try:
        # Для простоты используем datetime.fromisoformat (поддерживает '2026-03-04T15:30:00')
        dt = datetime.fromisoformat(date_str)
    except ValueError:
        # Если не получилось, пробуем другие распространённые форматы
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')  # только дата (будет 00:00:00)
            except ValueError:
                raise ValidationError(f"{field_name} has invalid format. Use ISO 8601 (e.g., 2026-03-04T15:30:00).")

    # Приводим к timezone-aware, если требуется (сравнение с timezone.now() будет корректным)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())

    # Проверка, что дата не в прошлом
    if dt < timezone.now():
        raise ValidationError(f"{field_name} cannot be in the past.")
    return dt


def index(request):
    data = {'menu': menu, 'title': 'EVENTS'}
    if 'id' in request.GET:
        data = {'finding_per_id': request.GET['id']}
    return JsonResponse(data=data)


@csrf_exempt
def events_handler(request):
    print(request)
    data = {'GET': '((('}

    if request.method == 'POST':
        print('Получен post запрос!')
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        print(data)

        title = data.get('title')
        if not title:
            return JsonResponse({'error': 'Missing title'}, status=400)
        description = data.get('description')
        if not description:
            return JsonResponse({'error': 'Missing description'}, status=400)
        purposed_datetime = data.get('purposed_datetime')
        if not purposed_datetime:
            return JsonResponse({'error': 'Missing purposed_datetime'}, status=400)
        try:
            purposed_datetime = parse_and_validate_datetime(purposed_datetime)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        try:
            event = Events.objects.create(
                title=title,
                description=description,
                purposed_datetime=purposed_datetime,
            )
        except Exception as e:
            return JsonResponse({'error': f'Database error: {e}'}, status=500)

        response_data = {
            'id': event.pk,
            'title': event.title,
            'description': event.description,
            'purposed_datetime': event.purposed_datetime,
            'created_datetime': event.created_datetime,
            'updated_datetime': event.updated_datetime,
        }

        return JsonResponse(
            data=response_data,
            json_dumps_params={'ensure_ascii': False},
            status=201,
        )
    elif request.method == 'PUT':
        print('Получен put запрос!')
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        print(data)
        event_id = data.get('event_id')
        if not event_id:
            return JsonResponse({'error': 'Missing event_id'}, status=400)
        try:
            event = Events.objects.get(pk=event_id)
        except Events.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)

        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'purposed_datetime' in data:
            event.purposed_datetime = data['purposed_datetime']
        try:
            event.save()
        except Exception as e:
            return JsonResponse(
                {'error': f'Database error: {str(e)}'},
                status=500,
            )
        response_data = {
            'id': event.pk,
            'title': event.title,
            'description': event.description,
            'purposed_datetime': event.purposed_datetime,
            'created_datetime': event.created_datetime,
            'updated_datetime': event.updated_datetime,
        }
        return JsonResponse(
            data=response_data,
            json_dumps_params={'ensure_ascii': False},
            status=200,
        )
    elif request.method == 'DELETE':
        print('Получен delete запрос!')
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        print(data)

        event_id = data.get('event_id')
        if not event_id:
            return JsonResponse({'error': 'Missing event_id'}, status=400)
        
        try:
            event = Events.objects.get(pk=event_id)
        except Events.DoesNotExist as e:
            return JsonResponse({'error': f'Event not found: {e}'}, status=404)
        try:
            event.delete()
        except Exception as e:
            return JsonResponse({'error': f'Database error: {e}'}, status=500)

        return JsonResponse(
            data=data,
            json_dumps_params={'ensure_ascii': False},
            status=204,
        )

    elif request.method == 'GET':
        print('Получен get запрос!')
        data: dict = {}
        event_id = request.GET.get('id')
        if event_id:
            data['event_id'] = event_id
            try:
                event = Events.objects.get(pk=event_id)
                data_event = {
                    'id': event.pk,
                    'title': event.title,
                    'description': event.description,
                    'purposed_datetime': event.purposed_datetime,
                    'created_datetime': event.created_datetime,
                    'updated_datetime': event.updated_datetime,
                }

                return JsonResponse(data_event)
            except Events.DoesNotExist as e:
                return JsonResponse({'error': f'Event not found: {e}'}, status=404)
            except Exception as e:
                return JsonResponse({'Uncnown error': e}, status=400)
        else:
            limit = request.GET.get('limit', 5)
            data['limit'] = limit
            if int(limit) < 0:
                return JsonResponse({'error': 'Limit should be > 0'}, status=400)
            try:
                events = Events.objects.filter(
                    purposed_datetime__gte=timezone.now(),
                ).order_by('purposed_datetime')
                data_events = []
                if int(limit) > len(events):
                    limit = len(events)
                for event in events[:int(limit)]:
                    data_events.append({
                        'id': event.pk,
                        'title': event.title,
                        'description': event.description,
                        'purposed_datetime': event.purposed_datetime,
                        'created_datetime': event.created_datetime,
                        'updated_datetime': event.updated_datetime,
                    })

                return JsonResponse(data_events, safe=False)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
