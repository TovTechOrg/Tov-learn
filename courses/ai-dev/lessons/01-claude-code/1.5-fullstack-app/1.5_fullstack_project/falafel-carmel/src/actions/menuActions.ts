'use server'

import { type MenuItem } from '@prisma/client'
import { revalidatePath } from 'next/cache'
import { prisma } from '@/lib/prisma'

// ─── Read ─────────────────────────────────────────────────────────────────────

export async function getMenuItems(): Promise<MenuItem[]> {
  try {
    return await prisma.menuItem.findMany({
      orderBy: { createdAt: 'asc' },
    })
  } catch (error) {
    console.error('[getMenuItems]', error)
    throw new Error('Failed to fetch menu items')
  }
}

// ─── Create ───────────────────────────────────────────────────────────────────

type ActionResult = { success: boolean; message: string }

export async function createMenuItem(formData: FormData): Promise<ActionResult> {
  const name        = formData.get('name')
  const description = formData.get('description')
  const price       = formData.get('price')
  const isSpicy     = formData.get('isSpicy')

  if (!name || !description || !price) {
    return { success: false, message: 'יש למלא שם, תיאור ומחיר' }
  }

  const parsedPrice = parseFloat(price as string)
  if (isNaN(parsedPrice) || parsedPrice < 0) {
    return { success: false, message: 'המחיר חייב להיות מספר חיובי' }
  }

  try {
    await prisma.menuItem.create({
      data: {
        name:        name as string,
        description: description as string,
        price:       parsedPrice,
        isSpicy:     isSpicy === 'on' || isSpicy === 'true',
      },
    })
    revalidatePath('/')
    return { success: true, message: 'המנה התווספה בהצלחה!' }
  } catch (error) {
    console.error('[createMenuItem]', error)
    return { success: false, message: 'שגיאה בשמירת המנה, נסה שוב' }
  }
}

// ─── Delete ───────────────────────────────────────────────────────────────────

export async function deleteMenuItem(id: string): Promise<void> {
  if (!id) {
    throw new Error('MenuItem id is required')
  }

  try {
    await prisma.menuItem.delete({
      where: { id },
    })
    revalidatePath('/')
  } catch (error) {
    console.error('[deleteMenuItem]', error)
    throw new Error('Failed to delete menu item')
  }
}
