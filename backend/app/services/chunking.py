def process_chunk(chunk: list[dict]) -> dict:
    if not chunk:
        return {}
    start_time = chunk[0]['start']
    end_time = chunk[-1]['start'] + chunk[-1]['duration']
    content = " ".join(s['text'] for s in chunk)
    return {
        "start": round(start_time, 2),
        "end": round(end_time, 2),
        "content": content
    }


def chunk_transcript(segments: list, window_seconds: float = 120.0, overlap_seconds: float = 30.0) -> list:
    chunks = []
    curr_chunk = []
    chunk_start: float = segments[0]['start']

    for seg in segments:
        seg_end = seg['start'] + seg['duration']
        if seg_end > chunk_start + window_seconds:
            chunks.append(process_chunk(curr_chunk))
            overlap_start = max(0.0, chunks[-1]['end'] - overlap_seconds)
            curr_chunk = [
                s for s in curr_chunk if s['start']+s['duration'] > overlap_start
            ]
            chunk_start = curr_chunk[0]['start'] if curr_chunk else seg['start']
        curr_chunk.append(seg)
    if curr_chunk:
        chunks.append(process_chunk(curr_chunk))
    return chunks

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"