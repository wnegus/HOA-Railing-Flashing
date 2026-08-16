create table public.railing_flashing_votes (
  id uuid primary key default gen_random_uuid(),
  color_id text not null,
  points int not null,
  voter_name text,
  created_at timestamptz not null default now()
);

alter table public.railing_flashing_votes enable row level security;

create policy "Public can read railing flashing votes" on public.railing_flashing_votes
  for select using (true);

create policy "Public can insert railing flashing votes" on public.railing_flashing_votes
  for insert with check (true);

create policy "Public can delete railing flashing votes" on public.railing_flashing_votes
  for delete using (true);
